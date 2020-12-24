# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/forms/BaseForms.py
# Compiled at: 2012-01-05 21:48:33
from lib.djangoFormImports import widgets, fields, extras
from django.forms import Form, BaseForm
from google.appengine.ext.db.djangoforms import ModelForm
from models.BaseModels import *

class PersonForm(ModelForm):

    class Meta:
        model = Person


class LoginForm(Form):
    RedirectUrl = fields.CharField(widget=widgets.HiddenInput, required=False)
    Email = fields.CharField(required=True)
    Password = fields.Field(required=True, widget=widgets.PasswordInput)


class RoleForm(ModelForm):

    class Meta:
        model = Role


class RoleAssociationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RoleAssociationForm, self).__init__(*args, **kwargs)
        self.fields['Person'].queryset = Person.all().fetch(limit=100)

    class Meta:
        model = RoleAssociation


from django.forms import Form

class InvitationForm(Form):
    Email = fields.EmailField(required=True)