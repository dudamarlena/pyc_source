# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/fields/array.py
# Compiled at: 2018-07-31 07:22:18
# Size of source mod 2**32: 1080 bytes
from django import forms
from django.forms import SelectMultiple
try:
    from django.contrib.postgres.fields import ArrayField
except ImportError:

    class ArrayField(object):
        pass


__all__ = ['ArrayField', 'ArrayChoiceField']

class ArraySelectMultiple(SelectMultiple):

    def value_omitted_from_data(self, data, files, name):
        return False


class ArrayChoiceField(ArrayField):
    __doc__ = "\n    A field that allows us to store an array of choices.\n     \n    Uses Django 1.9's postgres ArrayField\n    and a MultipleChoiceField for its formfield.\n    "

    def formfield(self, **kwargs):
        defaults = {'form_class':forms.TypedMultipleChoiceField, 
         'choices':self.base_field.choices, 
         'coerce':self.base_field.to_python, 
         'widget':ArraySelectMultiple}
        defaults.update(kwargs)
        return (super(workon.ArrayField, self).formfield)(**defaults)