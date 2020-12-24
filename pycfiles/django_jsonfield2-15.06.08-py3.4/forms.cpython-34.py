# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonfield2/forms.py
# Compiled at: 2015-06-02 20:24:25
# Size of source mod 2**32: 939 bytes
import json
from django import forms
from django.utils import six
from .widgets import JSONWidget

class JSONFormField(forms.CharField):
    empty_values = [
     None, '']

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = JSONWidget
        super(JSONFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, six.string_types) and value:
            try:
                return json.loads(value)
            except ValueError as exc:
                raise forms.ValidationError('JSON decode error: %s' % (six.u(exc.args[0]),))

        else:
            return value

    def validate(self, value):
        if value in self.empty_values:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'], code='required')