# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/app_plugins/forms.py
# Compiled at: 2008-10-17 00:15:13
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from app_plugins.models import PluginPoint, Plugin, LABEL_RE

def validate_label(value):
    if not LABEL_RE.search(value):
        raise forms.ValidationError(ugettext("This value must contain only letters, numbers, underscores, and '.' dots."))
    else:
        return value


class AdminPluginPointForm(forms.ModelForm):

    class Meta:
        model = PluginPoint

    def clean_label(self):
        value = self.cleaned_data['label']
        return validate_label(value)


class AdminPluginForm(forms.ModelForm):

    class Meta:
        model = Plugin

    def clean_label(self):
        value = self.cleaned_data['label']
        return validate_label(value)