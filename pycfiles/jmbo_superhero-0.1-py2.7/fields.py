# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superhero/fields.py
# Compiled at: 2015-05-05 00:01:33
from django.core import validators
from django.forms.fields import FileField
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from superhero.widgets import FileMultiInput

class FileMultiField(FileField):
    widget = FileMultiInput
    default_error_messages = FileField.default_error_messages.copy()
    default_error_messages['max_size'] = _('All uploaded files must be smaller than %(max_size)s bytes.')

    def __init__(self, *args, **kwargs):
        self.max_size = kwargs.pop('max_size', None)
        super(FileMultiField, self).__init__(*args, **kwargs)
        return

    def to_python(self, data):
        if data in validators.EMPTY_VALUES:
            return
        else:
            for d in data:
                try:
                    file_name = d.name
                    file_size = d.size
                except AttributeError:
                    raise ValidationError(self.error_messages['invalid'])

                if self.max_length is not None and len(file_name) > self.max_length:
                    error_values = {'max': self.max_length, 'length': len(file_name)}
                    raise ValidationError(self.error_messages['max_length'] % error_values)
                if self.max_size is not None and file_size > self.max_size:
                    error_values = {'max_size': self.max_size}
                    raise ValidationError(self.error_messages['max_size'] % error_values)
                if not file_name:
                    raise ValidationError(self.error_messages['invalid'])
                if not file_size:
                    raise ValidationError(self.error_messages['empty'])

            return data