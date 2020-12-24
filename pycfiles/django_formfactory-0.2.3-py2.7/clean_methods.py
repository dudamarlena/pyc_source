# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/tests/formfactoryapp/clean_methods.py
# Compiled at: 2017-09-07 07:30:48
from django import forms
from formfactory import clean_methods

@clean_methods.register
def check_if_values_match(form_instance, **kwargs):
    """Clean method for when a contact updates password.
    """
    first_field = form_instance.cleaned_data['first_field']
    second_field = form_instance.cleaned_data['second_field']
    if not first_field == second_field:
        raise forms.ValidationError('The values you entered are not equal.')