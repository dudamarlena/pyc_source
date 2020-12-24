# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/irekua_filters/sites.py
# Compiled at: 2019-12-05 13:03:33
# Size of source mod 2**32: 1004 bytes
from django import forms
from django.db import models
import django.utils.translation as _
from django_filters import FilterSet, DateFilter
from irekua_database.models import Site

class Filter(FilterSet):

    class Meta:
        model = Site
        fields = {'name':[
          'exact', 'icontains'], 
         'locality':[
          'exact'], 
         'locality__name':[
          'icontains'], 
         'latitude':[
          'gt', 'lt'], 
         'longitude':[
          'gt', 'lt'], 
         'altitude':[
          'gt', 'lt'], 
         'created_on':[
          'gt', 'lt']}
        filter_overrides = {models.DateTimeField: {'filter_class':DateFilter, 
                                'extra':lambda f: {'widget': forms.DateInput(attrs={'class': 'datepicker'})}}}


search_fields = ('name', 'locality__name')
ordering_fields = (
 (
  'created_on', _('added on')),
 (
  'name', _('name')),
 (
  'locality', _('locality')))