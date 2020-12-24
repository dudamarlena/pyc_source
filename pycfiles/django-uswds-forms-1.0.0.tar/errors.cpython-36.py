# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/app/examples/errors.py
# Compiled at: 2017-05-16 08:15:53
# Size of source mod 2**32: 957 bytes
"""
Errors

This example shows how errors are automatically given proper styling,
thanks to uswds_forms.UswdsForm and Django 1.11's new form rendering API.
"""
from django.shortcuts import render
from django import forms
import uswds_forms

class MyForm(uswds_forms.UswdsForm):
    text = forms.CharField(label='Text input label')
    checkbox = forms.BooleanField(label='I agree to the terms of service')

    def clean(self):
        super().clean()
        self.add_error('text', 'Helpful error message #1')
        self.add_error('text', 'Helpful error message #2')
        self.add_error(None, 'Helpful non-field error message #1')
        self.add_error(None, 'Helpful non-field error message #2')


def view(request):
    form = MyForm({'text': 'blah'})
    form.is_valid()
    return render(request, 'examples/errors.html', {'form': form})