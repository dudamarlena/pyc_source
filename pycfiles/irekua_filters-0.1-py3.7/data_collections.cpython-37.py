# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_filters/data_collections/data_collections.py
# Compiled at: 2019-10-28 01:48:49
# Size of source mod 2**32: 1194 bytes
from django import forms
from django.db import models
import django.utils.translation as _
from django_filters import FilterSet
from django_filters import DateFilter
from irekua_database.models import Collection

class Filter(FilterSet):

    class Meta:
        model = Collection
        fields = {'collection_type':[
          'exact'], 
         'name':[
          'icontains'], 
         'institution':[
          'exact'], 
         'institution__institution_name':[
          'exact', 'icontains'], 
         'institution__institution_code':[
          'exact', 'icontains'], 
         'institution__country':[
          'icontains'], 
         'is_open':[
          'exact'], 
         'created_on':[
          'gt', 'lt']}
        filter_overrides = {models.DateTimeField: {'filter_class':DateFilter, 
                                'extra':lambda f: {'widget': forms.DateInput(attrs={'class': 'datepicker'})}}}


search_fields = ('name', 'collection_type__name', 'institution__institution_name',
                 'institution__institution_code')
ordering_fields = (
 (
  'created_on', _('created on')),
 (
  'name', _('name')))