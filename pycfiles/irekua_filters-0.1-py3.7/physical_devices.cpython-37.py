# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_filters/devices/physical_devices.py
# Compiled at: 2019-10-27 23:36:35
# Size of source mod 2**32: 1162 bytes
from django import forms
from django.db import models
import django.utils.translation as _
from django_filters import FilterSet, DateFilter
from irekua_database.models import PhysicalDevice

class Filter(FilterSet):

    class Meta:
        model = PhysicalDevice
        fields = {'serial_number':[
          'exact', 'icontains'], 
         'device__brand__name':[
          'exact', 'icontains'], 
         'device__model':[
          'exact', 'icontains'], 
         'bundle':[
          'exact'], 
         'identifier':[
          'exact', 'icontains'], 
         'created_on':[
          'lt', 'gt']}
        filter_overrides = {models.DateTimeField: {'filter_class':DateFilter, 
                                'extra':lambda f: {'widget': forms.DateInput(attrs={'class': 'datepicker'})}}}


search_fields = ('device__brand__name', 'device__model', 'identifier')
ordering_fields = (
 (
  'created_on', _('added on')),
 (
  'serial_number', _('serial number')),
 (
  'identifier', _('custom id')),
 (
  'device__brand__name', _('brand')),
 (
  'device__model', _('model')))