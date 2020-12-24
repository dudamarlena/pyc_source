# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gustavofonseca/prj/github/scielo-django-extensions/scielo_extensions/fields.py
# Compiled at: 2012-03-19 13:27:34
import re
from django import forms
from django.utils.translation import ugettext_lazy as _

class ISSNField(forms.CharField):
    default_error_messages = {'invalid': _('Enter a valid ISSN.')}
    regex = '[0-9]{4}-[0-9]{3}[0-9X]{1}$'

    def clean(self, value):
        if value is not '' and value is not None:
            result = re.match(self.regex, value)
            if result is None:
                raise forms.ValidationError(self.error_messages['invalid'])
        return value