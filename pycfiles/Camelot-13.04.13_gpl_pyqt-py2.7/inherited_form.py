# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/form/inherited_form.py
# Compiled at: 2013-04-11 17:47:52
from copy import deepcopy
from camelot.view import forms
from nested_form import Admin

class InheritedAdmin(Admin):
    form_display = deepcopy(Admin.form_display)
    form_display.add_tab('Work', forms.Form(['employers', 'directed_organizations', 'shares']))