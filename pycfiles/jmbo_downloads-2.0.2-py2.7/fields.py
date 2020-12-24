# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/downloads/fields.py
# Compiled at: 2015-04-21 15:31:46
import re
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from south.modelsinspector import add_introspection_rules

class ColourField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        kwargs['help_text'] = 'Hexadecimal format, e.g. #f0d245'
        super(ColourField, self).__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs['validators'] = [
         RegexValidator('^#[\\da-f]{6}$', _('Enter a hexadecimal-format colour.'), 'Invalid')]
        return super(ColourField, self).formfield(*args, **kwargs)


add_introspection_rules([], ['^downloads\\.fields\\.ColourField'])