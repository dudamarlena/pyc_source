# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/forms.py
# Compiled at: 2015-08-31 20:53:03
__author__ = 'marcos.medeiros'
from django import forms
from rapid.models import Profile, Application
from rapid.wrappers import FieldData
from rapid.widgets import RapidReadOnly, RapidRelationReadOnly, RapidSelector

class ManageUsers(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {'application': RapidRelationReadOnly(Application), 
           'name': RapidReadOnly(), 
           'description': RapidReadOnly, 
           'users': RapidSelector(FieldData.from_model(Profile, 'users'))}