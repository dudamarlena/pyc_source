# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/irekua_filters/data_collections/data_collections.py
# Compiled at: 2020-01-17 22:57:45
# Size of source mod 2**32: 959 bytes
import django.utils.translation as _
from django_filters import FilterSet
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
          'gt', 'lt'], 
         'collectiondevice__physical_device':[
          'exact'], 
         'collectionsite__site':[
          'exact']}


search_fields = ('name', 'description', 'collection_type__name', 'institution__institution_name',
                 'institution__institution_code')
ordering_fields = (
 (
  'created_on', _('created on')),
 (
  'name', _('name')))