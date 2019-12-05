from django import forms

from import_export.resources import Resource


class ResourceFieldsForm(forms.Form):
    resource = Resource
    field = forms.ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        recipient_headers = [[field, field] for field in self.resource.fields]
        CHOICE = [('-----', '------')] + recipient_headers
        self.fields['field'].choices = CHOICE
