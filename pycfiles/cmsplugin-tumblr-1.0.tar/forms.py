# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jrief/Workspace/virtualenvs/gfg/src/cmsplugin-text-wrapper/cmsplugin_text_wrapper/forms.py
# Compiled at: 2013-07-25 09:20:29
from cmsplugin_text_wrapper.models import TextWrapper
from django import forms
from django.forms.models import ModelForm

class TextForm(ModelForm):
    body = forms.CharField()

    class Meta:
        model = TextWrapper
        fields = ('wrapper', 'classes', 'body')
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')