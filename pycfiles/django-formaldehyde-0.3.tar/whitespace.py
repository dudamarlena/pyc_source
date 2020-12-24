# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kraken/Projects/websites/django-formaldehyde/formaldehyde/formaldehyde/whitespace.py
# Compiled at: 2015-01-30 05:01:05
from __future__ import unicode_literals
from django import forms
from django.utils import six

class StripWhitespaceFormMixin(object):
    """
    Strip whitespace automatically in all form fields after a full_clean call
    """

    def strip_whitespace_from_data(self):
        assert isinstance(self, forms.BaseForm)
        if hasattr(self, b'data') and self.data:
            data = self.data.copy()
            if hasattr(self.data, b'lists'):
                for key, values in self.data.lists():
                    new_values = []
                    for v in values:
                        if isinstance(v, six.text_type):
                            v = v.strip()
                        new_values.append(v)

                    data.setlist(key, new_values)

            else:
                for key, value in six.iteritems(self.data):
                    if isinstance(value, six.text_type):
                        value = value.strip()
                    data[key] = value

            self.data = data