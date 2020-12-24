# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_filters/data_collections/collection_sampling_events.py
# Compiled at: 2019-10-28 00:08:06
# Size of source mod 2**32: 1583 bytes
from django import forms
from django.db import models
import django.utils.translation as _
from django_filters import FilterSet
from django_filters import DateFilter
from django_filters import BooleanFilter
from irekua_database.models import SamplingEvent

class Filter(FilterSet):
    is_own = BooleanFilter(method='user_owns_object',
      label=(_('Mine')),
      widget=(forms.CheckboxInput()))

    class Meta:
        model = SamplingEvent
        fields = {'created_by':[
          'exact'], 
         'created_by__username':[
          'icontains'], 
         'created_by__first_name':[
          'icontains'], 
         'created_by__last_name':[
          'icontains'], 
         'sampling_event_type':[
          'exact'], 
         'collection_site__site__name':[
          'icontains'], 
         'started_on':[
          'gt', 'lt'], 
         'ended_on':[
          'gt', 'lt'], 
         'created_on':[
          'gt', 'lt']}
        filter_overrides = {models.DateTimeField: {'filter_class':DateFilter, 
                                'extra':lambda f: {'widget': forms.DateInput(attrs={'class': 'datepicker'})}}}

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(created_by=user)
        return queryset


search_fields = ('sampling_event_type__name', 'collection_site__internal_id')
ordering_fields = (
 (
  'created_on', _('added on')),
 (
  'started_on', _('started on')),
 (
  'ended_on', _('ended on')))