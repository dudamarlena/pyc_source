# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/django_enums/forms/fields.py
# Compiled at: 2016-06-24 04:50:27
from __future__ import division, print_function, absolute_import, unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _

class EnumField(forms.ChoiceField):
    widget = forms.Select
    default_error_messages = {b'invalid_choice': _(b'Select a valid choice. %(value)s is not one of the available choices.')}

    def __init__(self, enum, required=True, widget=None, label=None, initial=None, help_text=b'', *args, **kwargs):
        super(EnumField, self).__init__(required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs)
        self.enum = enum

    def to_python(self, value):
        """Returns an Enum object."""
        if value in self.empty_values:
            return b''
        return self.enum.get_by_key(value)

    def valid_value(self, value):
        """Check to see if the provided value is a valid choice"""
        enum_value = self.enum.get_by_key(value)
        return isinstance(enum_value, self.enum)