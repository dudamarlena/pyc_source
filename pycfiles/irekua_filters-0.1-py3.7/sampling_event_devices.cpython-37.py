# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_filters/sampling_events/sampling_event_devices.py
# Compiled at: 2019-10-27 23:36:35
# Size of source mod 2**32: 1400 bytes
from django import forms
from django.db import models
import django.utils.translation as _
from django_filters import FilterSet, DateFilter
from django_filters import BooleanFilter
from irekua_database.models import SamplingEventDevice

class Filter(FilterSet):
    is_own = BooleanFilter(method='user_owns_object',
      label=(_('Mine')),
      widget=(forms.CheckboxInput()))

    class Meta:
        model = SamplingEventDevice
        fields = {'created_by__username':[
          'icontains'], 
         'created_by__first_name':[
          'icontains'], 
         'created_by__last_name':[
          'icontains'], 
         'collection_device__physical_device__device__brand__name':[
          'icontains'], 
         'collection_device__physical_device__device__model':[
          'icontains'], 
         'collection_device__physical_device__device__device_type':[
          'exact'], 
         'created_on':[
          'gt', 'lt']}

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(collection_device__created_by=user)
        return queryset


search_fields = ('collection_device__physical_device__device__serial_number', 'collection_device__physical_device__device__brand__name',
                 'collection_device__physical_device__device__model')
ordering_fields = (
 (
  'created_on', _('added on')),)