# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Aaswaini Dev\PycharmProjects\FinanceCRM\apps\csv_importer\forms.py
# Compiled at: 2020-04-22 11:39:13
# Size of source mod 2**32: 2292 bytes
import io
from django import forms
from django.db.models import ForeignKey
from .utils import get_required_fields, get_optional_fields

def validate_file_for_fields(required_fields):

    def validate_file_for_fields_inner(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError('Only CSV file is accepted')
        import csv
        decoded_file = value.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=',', quotechar='|')
        row = next(reader)
        for field in required_fields:
            if field not in row:
                raise forms.ValidationError(" '%s' field is not present in the uploaded file. Required field(s) is/are: %s " % (
                 field, ', '.join(required_fields)))

        value.seek(0)

    return validate_file_for_fields_inner


class CSVUploadForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        (super().__init__)(*args, **kwargs)
        all_model_fields = self.model._meta.get_fields()
        all_fk_model_fields = []
        all_non_fk_model_fields = []
        for field in all_model_fields:
            if isinstance(self.model._meta.get_field(field.name), ForeignKey) and hasattr(field, 'blank') and not field.blank:
                all_fk_model_fields.append(field.name)
            else:
                all_non_fk_model_fields.append(field.name)

        for field in all_fk_model_fields:
            if field in self.model.fk_handle_by_id:
                pass
            else:
                model = self.model._meta.get_field(field).remote_field.model
                self.fields[field] = forms.ModelChoiceField(queryset=(model.objects.all()))

        self.fields['csv_file'] = forms.FileField()
        required_fields = get_required_fields(self.model)
        optional_fields = get_optional_fields(self.model)
        self.fields['csv_file'].help_text = 'Required field(s) is/are: %s AND Optional fields: %s' % (
         ', '.join(required_fields), ', '.join(optional_fields))
        self.fields['csv_file'].validators = [validate_file_for_fields(required_fields)]