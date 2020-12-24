# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/postgres/forms/hstore.py
# Compiled at: 2019-02-14 00:35:16
import json
from django import forms
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.translation import ugettext_lazy as _
__all__ = [
 'HStoreField']

class HStoreField(forms.CharField):
    """
    A field for HStore data which accepts dictionary JSON input.
    """
    widget = forms.Textarea
    default_error_messages = {'invalid_json': _('Could not load JSON data.'), 
       'invalid_format': _('Input must be a JSON dictionary.')}

    def prepare_value(self, value):
        if isinstance(value, dict):
            return json.dumps(value)
        return value

    def to_python(self, value):
        if not value:
            return {}
        else:
            if not isinstance(value, dict):
                try:
                    value = json.loads(value)
                except ValueError:
                    raise ValidationError(self.error_messages['invalid_json'], code='invalid_json')

            if not isinstance(value, dict):
                raise ValidationError(self.error_messages['invalid_format'], code='invalid_format')
            for key, val in value.items():
                if val is not None:
                    val = six.text_type(val)
                value[key] = val

            return value

    def has_changed(self, initial, data):
        """
        Return True if data differs from initial.
        """
        initial_value = self.to_python(initial)
        return super(HStoreField, self).has_changed(initial_value, data)