# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/irekua_filters/data_collections/collection_users.py
# Compiled at: 2020-01-09 14:54:59
# Size of source mod 2**32: 1127 bytes
import django.utils.translation as _
from django_filters import FilterSet
from irekua_database.models import CollectionUser

class Filter(FilterSet):

    class Meta:
        model = CollectionUser
        fields = {'role':[
          'exact'], 
         'user':[
          'exact'], 
         'user__institution':[
          'exact'], 
         'user__institution__institution_name':[
          'icontains'], 
         'user__institution__institution_code':[
          'icontains'], 
         'user__institution__country':[
          'exact'], 
         'user__first_name':[
          'icontains'], 
         'user__last_name':[
          'icontains'], 
         'user__username':[
          'icontains'], 
         'user__email':[
          'icontains'], 
         'created_on':[
          'gt', 'lt']}


search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email',
                 'user__institution__institution_name', 'user__institution__institution_code')
ordering_fields = (
 (
  'created_on', _('added on')),
 (
  'user__first_name', _('first name')),
 (
  'user__last_name', _('last name')),
 (
  'user__username', _('username')))