# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/custom_fields.py
# Compiled at: 2010-08-21 21:05:32
"""
This is file containing custom model fields.

This is modified from http://stackoverflow.com/questions/3397400/django-model-field-for-storing-a-list-of-floats/3398546#3398546
"""
import re
from django.db.models import CharField
from django.core import validators
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^mousedb\\.custom_fields\\.CommaSeparatedFloatField'])
comma_separated_float_list_re = re.compile('^([-+]?\\d*\\.?\\d+[,\\s]*)+$')
validate_comma_separated_float_list = validators.RegexValidator(comma_separated_float_list_re, 'Enter only floats separated by commas.', 'invalid')

class CommaSeparatedFloatField(CharField):
    """A custom field for comma separated float values."""
    default_validators = [
     validate_comma_separated_float_list]
    description = 'Comma-separated floats'

    def formfield(self, **kwargs):
        defaults = {'error_messages': {'invalid': 'Enter only floats separated by commas.'}}
        defaults.update(kwargs)
        return super(CommaSeparatedFloatField, self).formfield(**defaults)