from django.contrib import admin
from importer.models import CsvFile
# Register your models here.


@admin.register(CsvFile)
class CsvFile(admin.ModelAdmin):
    list_display = (
        'id',
        "file",
    )
