# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-pagetimer/pagetimer/forms.py
# Compiled at: 2016-05-10 09:39:30
from datetime import datetime, timedelta
from django import forms
from django.forms.widgets import DateTimeInput

class PurgeForm(forms.Form):
    timestamp = forms.DateTimeField(label='purge entries older than (YYYY-MM-DD hh:mm:ss):', widget=DateTimeInput(format='%Y-%m-%d %H:%M:%S'), initial=datetime.now() - timedelta(days=1))