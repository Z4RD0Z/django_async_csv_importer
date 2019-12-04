import csv
import logging
import os

from celery import shared_task
from django.shortcuts import get_object_or_404
from tablib import Dataset

@shared_task
def import_csv(file_pk, values, resource):
    """ Get file and its path, after try to import data and test the dataset.
    If it's right import dataset in database.

    :param file_pk : send by post in ConfirmCSVImport.
    :param values: send by formset in ConfirmCSVImport, new headers values.
    :return the import result """

    import_resource = resource()

    file = get_object_or_404(CsvFile, pk=file_pk)
    filename = file.file

    relative_path = "%s" % filename
    full_path = "uploads/%s" % relative_path

    dataset = Dataset()
    imported_data = dataset.load(open(full_path).read(), format='csv')

    dataset.headers.clear()

    for value in values:
        dataset.headers.append(value)

    try:
        os.remove(full_path)
    
    except FileNotFoundError:
        print("File not Found")

    try:
        
        result = import_resource.import_data(
            dataset, dry_run=False)  # Actually import now

        logging.getLogger("info_logger").info(f"{result}")

        with open('test.csv', 'w') as testfile:
            fieldnames = ['Riga', 'Campo', 'Errore']
            writer = csv.DictWriter(testfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in result.invalid_rows:
                d = {}
                d['Riga'] = row.number
                for k, v in row.error:
                    d['Campo'] = k
                    d['Errore'] = v
                writer.writerow(d)

        return True

    except AttributeError as e:

        logging.getLogger("error_logger").error(repr(e))
        i = {}

        i['erorre'] = repr(e)

        with open('mycsvfile.csv', 'w') as file:
            w = csv.DictWriter(file, i.keys())
            w.writeheader()
            w.writerow(i)

        return False

    finally:
        CsvFile.objects.get(pk=file_pk).delete()
