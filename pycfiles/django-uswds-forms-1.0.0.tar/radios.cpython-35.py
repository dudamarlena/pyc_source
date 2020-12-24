# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/app/examples/radios.py
# Compiled at: 2017-05-12 17:41:34
# Size of source mod 2**32: 819 bytes
"""
Radio buttons

This example shows how to render radio buttons using the
uswds_forms.UswdsRadioSelect widget.
"""
from django.shortcuts import render
from django import forms
import uswds_forms

class MyForm(uswds_forms.UswdsForm):
    president = forms.ChoiceField(label='Who is your favorite president?', widget=uswds_forms.UswdsRadioSelect, help_text="If you don't see your favorite, just pick your favorite of the ones we've listed.", choices=(('washington', 'George Washington'),
                                                                                                                                                                                                                        ('adams', 'John Adams'),
                                                                                                                                                                                                                        ('jefferson', 'Thomas Jefferson')))


def view(request):
    return render(request, 'examples/radios.html', {'form': MyForm() if request.method == 'GET' else MyForm(request.POST)})