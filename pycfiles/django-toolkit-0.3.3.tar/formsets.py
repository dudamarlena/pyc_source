# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/forms/formsets.py
# Compiled at: 2013-03-19 00:20:36
from django.forms.formsets import DELETION_FIELD_NAME
from django.forms.widgets import HiddenInput
from django.forms.models import BaseModelFormSet

class HiddenDeleteModelFormSet(BaseModelFormSet):

    def add_fields(self, form, index):
        super(HiddenDeleteModelFormSet, self).add_fields(form, index)
        form.fields[DELETION_FIELD_NAME].widget = HiddenInput()