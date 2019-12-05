from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here


class CsvFile(models.Model):
    file = models.FileField(
        upload_to='media/',
        validators=[FileExtensionValidator(allowed_extensions=['csv'])])
