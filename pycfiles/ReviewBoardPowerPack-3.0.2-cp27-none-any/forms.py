# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/forms.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import re
from datetime import datetime, time
from django import forms
from django.utils.timezone import make_aware, get_current_timezone
LIST_SPLIT_RE = re.compile(b',\\s*')

class BasicReportForm(forms.Form):
    start = forms.DateField(required=True, widget=forms.DateInput(attrs={b'size': b'10'}))
    end = forms.DateField(required=True, widget=forms.DateInput(attrs={b'size': b'10'}))
    users = forms.CharField(required=False)
    groups = forms.CharField(required=False)
    everyone = forms.BooleanField(initial=False, required=False)

    def _clean_date(self, data, time_offset):
        return make_aware(datetime.combine(data, time_offset), get_current_timezone())

    def _clean_list(self, data):
        return [ item for item in LIST_SPLIT_RE.split(data.strip()) if item
               ]

    def clean_start(self):
        return self._clean_date(self.cleaned_data[b'start'], time(0))

    def clean_end(self):
        return self._clean_date(self.cleaned_data[b'end'], time(23, 59, 59, 999999))

    def clean_users(self):
        return self._clean_list(self.cleaned_data[b'users'])

    def clean_groups(self):
        return self._clean_list(self.cleaned_data[b'groups'])