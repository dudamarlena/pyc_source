# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/postgres/forms/jsonb.py
# Compiled at: 2019-02-14 00:35:16
import json
from django import forms
from django.utils import six
from django.utils.translation import ugettext_lazy as _
__all__ = [
 'JSONField']

class InvalidJSONInput(six.text_type):
    pass


class JSONString(six.text_type):
    pass


class JSONField(forms.CharField):
    default_error_messages = {'invalid': _("'%(value)s' value must be valid JSON.")}
    widget = forms.Textarea

    def to_python(self, value):
        if self.disabled:
            return value
        else:
            if value in self.empty_values:
                return
            else:
                if isinstance(value, (list, dict, int, float, JSONString)):
                    return value
                try:
                    converted = json.loads(value)
                except ValueError:
                    raise forms.ValidationError(self.error_messages['invalid'], code='invalid', params={'value': value})

                if isinstance(converted, six.text_type):
                    return JSONString(converted)
                return converted

            return

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        try:
            return json.loads(data)
        except ValueError:
            return InvalidJSONInput(data)

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        return json.dumps(value)