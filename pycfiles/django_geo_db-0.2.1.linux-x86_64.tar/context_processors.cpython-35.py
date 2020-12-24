# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/context_processors.py
# Compiled at: 2018-02-04 15:10:23
# Size of source mod 2**32: 264 bytes
from django.conf import settings
from django_geo_db.services import GEO_DAL

def google_maps_api_key(request):
    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}


def google_maps_settings(request):
    return {'GM_SETTINGS': settings.GM_SETTINGS}