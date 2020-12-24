# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-places/vkontakte_places/lookups.py
# Compiled at: 2015-02-19 12:23:17
from ajax_select import LookupChannel
from models import City, Country

class VkontakteLookupChannel(LookupChannel):

    def get_pk(self, obj):
        return getattr(obj, 'remote_id')

    def get_objects(self, ids):
        ids = [ int(id) for id in ids ]
        return self.model.objects.filter(remote_id__in=ids)


class CityLookup(VkontakteLookupChannel):
    model = City
    search_field = 'name'

    def get_query(self, q, request):
        return self.model.remote.fetch(country=1, q=q)


class CountryLookup(VkontakteLookupChannel):
    model = Country
    search_field = 'name'