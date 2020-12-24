# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sw_logger/forms.py
# Compiled at: 2018-02-07 05:07:39
from django import forms
from . import consts
from . import tools

class Log(forms.Form):
    ACTION_CHOICES = [
     ('', '')] + list(consts.ACTION_CHOICES)
    LOG_LEVEL_CHOICES = [('', '')] + list(consts.LOG_LEVEL_CHOICES)
    datetime_from = forms.DateTimeField()
    datetime_to = forms.DateTimeField()
    action = forms.MultipleChoiceField(required=False, choices=consts.ACTION_CHOICES)
    level = forms.MultipleChoiceField(required=False, choices=consts.LOG_LEVEL_CHOICES)
    object_name = forms.MultipleChoiceField(required=False, choices=tools.get_models_choices())
    message = forms.CharField(required=False)
    username = forms.CharField(required=False)