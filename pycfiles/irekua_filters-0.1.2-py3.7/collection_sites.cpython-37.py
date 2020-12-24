# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/irekua_filters/data_collections/collection_sites.py
# Compiled at: 2020-01-17 22:42:55
# Size of source mod 2**32: 1391 bytes
from django import forms
import django.utils.translation as _
from django_filters import FilterSet
from django_filters import BooleanFilter
from irekua_database.models import CollectionSite

class Filter(FilterSet):
    is_own = BooleanFilter(method='user_owns_object',
      label=(_('Mine')),
      widget=(forms.CheckboxInput()))

    class Meta:
        model = CollectionSite
        fields = {'created_by':[
          'exact'], 
         'created_by__username':[
          'icontains'], 
         'created_by__first_name':[
          'icontains'], 
         'created_by__last_name':[
          'icontains'], 
         'site_type':[
          'exact'], 
         'site':[
          'exact'], 
         'site__altitude':[
          'gt', 'lt'], 
         'site__latitude':[
          'gt', 'lt'], 
         'site__longitude':[
          'gt', 'lt'], 
         'site__name':[
          'icontains'], 
         'site__locality':[
          'exact'], 
         'site__locality__name':[
          'icontains'], 
         'created_on':[
          'gt', 'lt']}

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(created_by=user)
        return queryset


search_fields = ('internal_id', 'site__name', 'site__locality__name', 'site_type__name')
ordering_fields = (
 (
  'created_on', _('added on')),
 (
  'internal_id', _('internal id')))