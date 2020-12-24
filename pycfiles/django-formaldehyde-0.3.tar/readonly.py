# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kraken/Projects/websites/django-formaldehyde/formaldehyde/formaldehyde/readonly.py
# Compiled at: 2015-01-30 05:01:05
from __future__ import unicode_literals
from django import forms

class ReadonlyFormMixin(object):
    """
    Mixin class to enable setting readonly of the form at runtime
    """

    def set_readonly(self, is_readonly=True):
        assert isinstance(self, forms.BaseForm)
        for field in self.fields:
            self.fields[field].is_readonly = is_readonly