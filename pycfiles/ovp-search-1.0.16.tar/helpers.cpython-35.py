# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-search/ovp_search/helpers.py
# Compiled at: 2017-05-08 18:10:05
# Size of source mod 2**32: 914 bytes
from django.conf import settings
from haystack import connection_router, connections
from haystack.inputs import Raw

def is_whoosh_backend():
    backend_alias = connection_router.for_read()
    return connections[backend_alias].__class__.__name__ == 'WhooshEngine'


def whoosh_raw(t):
    if is_whoosh_backend():
        return Raw('("{}")'.format(t))
    return t


def get_settings(string='OVP_SEARCH'):
    return getattr(settings, string, {})


def get_cities(queryset):
    cities = set()
    for item in queryset:
        for comp in item.address_components:
            if '-administrative_area_level_2' in comp or '-locality' in comp:
                city_name = comp.replace('-administrative_area_level_2', '').replace('-locality', '')
                cities.add(city_name)

    return cities