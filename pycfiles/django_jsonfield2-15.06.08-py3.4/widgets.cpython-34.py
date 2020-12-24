# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jsonfield2/widgets.py
# Compiled at: 2015-06-02 23:10:52
# Size of source mod 2**32: 467 bytes
import json
from django import forms
from django.utils import six
from .utils import default

class JSONWidget(forms.Textarea):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        if not isinstance(value, six.string_types):
            value = json.dumps(value, indent=2, default=default)
        return super(JSONWidget, self).render(name, value, attrs)


class JSONSelectWidget(forms.SelectMultiple):
    pass