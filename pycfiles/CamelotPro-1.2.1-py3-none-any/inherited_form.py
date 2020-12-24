# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/form/inherited_form.py
# Compiled at: 2013-04-11 17:47:52
from copy import deepcopy
from camelot.view import forms
from nested_form import Admin

class InheritedAdmin(Admin):
    form_display = deepcopy(Admin.form_display)
    form_display.add_tab('Work', forms.Form(['employers', 'directed_organizations', 'shares']))