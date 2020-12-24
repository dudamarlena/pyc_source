# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/managers.py
# Compiled at: 2018-02-11 10:49:56
# Size of source mod 2**32: 339 bytes
from django.db import models
from django_geo_db.utilities import get_lat_lon_from_string

class GeoCoordinateManager(models.Manager):

    def get_or_create_by_lat_lon(self, lat, lon):
        lat, lon = get_lat_lon_from_string('{0} {1}'.format(lat, lon))
        return super(GeoCoordinateManager, self).get_or_create(lat=lat, lon=lon)