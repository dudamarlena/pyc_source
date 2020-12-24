# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/sentry_dingding/forms.py
# Compiled at: 2019-05-08 09:14:34
from django import forms

class DingDingOptionsForm(forms.Form):
    access_token = forms.CharField(max_length=255, help_text='DingTalk robot access_token')