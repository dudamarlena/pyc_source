# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/forms/cmsForms.py
# Compiled at: 2011-12-28 06:28:19
__author__ = 'KMihajlov'
from google.appengine.ext.db.djangoforms import ModelForm
from django.forms import Form, BaseForm, fields, widgets
from django.forms.extras import widgets as extras
from models.cmsModels import *

class CMSContentForm(Form):

    def __init__(self, *args, **kwargs):
        super(CMSContentForm, self).__init__(*args, **kwargs)

    Title = fields.CharField(required=True, widget=widgets.TextInput(attrs={'style': 'width:500px;'}))
    Content = fields.CharField(widget=widgets.Textarea(), required=True)
    Tags = fields.CharField(required=False, widget=widgets.TextInput(attrs={'style': 'width:500px;'}))


class CMSMenuForm(Form):

    def __init__(self, *args, **kwargs):
        super(CMSMenuForm, self).__init__(*args, **kwargs)

    key = fields.Field(widget=widgets.HiddenInput, required=False)
    Name = fields.CharField(required=True, min_length=3)