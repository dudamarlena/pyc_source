# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/app/examples/checkboxes.py
# Compiled at: 2017-05-12 17:41:34
# Size of source mod 2**32: 637 bytes
"""
Multiple checkboxes

This example shows how to render groups of checkboxes using
a uswds_forms.UswdsMultipleChoiceField.
"""
from django.shortcuts import render
import uswds_forms

class MyForm(uswds_forms.UswdsForm):
    states = uswds_forms.UswdsMultipleChoiceField(label='What states have you visited?',
      required=False,
      choices=(('OH', 'Ohio'), ('IL', 'Illinois'), ('CA', 'California')))


def view(request):
    return render(request, 'examples/checkboxes.html', {'form': MyForm() if request.method == 'GET' else MyForm(request.POST)})