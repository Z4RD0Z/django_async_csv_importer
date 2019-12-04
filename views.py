import csv
from itertools import islice
from importer.tasks import import_csv
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from tablib import Dataset
from importer.models import CsvFile
# Create ymur views here.


class ConfirmCSVImport(FormView):

    form_class = None

    resource_model = None

    template_name = None

    def handle_uploaded_file(self):
        '''example logic from:
        https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/#handling-uploaded-files-with-a-model
        '''

        # Retrieve file's path
        file = get_object_or_404(CsvFile, pk=self.kwargs['pk'])
        filename = file.file

        relative_path = "%s" % filename
        full_path = "uploads/%s" % relative_path

        dataset = Dataset()

        # open csv and add first 5 rows to dataset
        with open(full_path) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for row in islice(csv_reader, 5):
                dataset.headers = row.keys()
                dataset.append(row.values())

        return dataset

    def get_context_data(self, **kwargs):
        data = self.handle_uploaded_file()

        # change number of formset on headers
        formset = self.form_class
        formset.extra = len(data.headers)

        # get data for template
        context = super().get_context_data(**kwargs)
        context['headers'] = data.headers
        context['data'] = data.dict
        context['formset'] = formset()

        return context

    def form_valid(self, form):
        values = []
        for f in form:
            value = f.cleaned_data['field']
            values.append(value)

        import_csv.delay(self.kwargs['pk'], values, self.resource_model)

        return super().form_valid(form)

