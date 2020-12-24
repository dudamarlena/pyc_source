# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/models/geo.py
# Compiled at: 2018-07-31 07:16:41
# Size of source mod 2**32: 795 bytes
import workon
from django.db import models
__all__ = [
 'Geo']

class Geo(models.Model):
    geo_address = models.CharField('Adresse géolocalisée', max_length=254, blank=True, null=True)
    geo_latitude = models.FloatField('lat', blank=True, null=True, db_index=True)
    geo_longitude = models.FloatField('lon', blank=True, null=True, db_index=True)
    geo_formatted_address = models.CharField('Adresse géocodée & formattée', max_length=254, blank=True, null=True)
    geo_data = workon.JSONField('Geodata', default={}, blank=True, null=True)
    google_place_id = models.CharField('Google place ID', max_length=254, blank=True, null=True)
    google_place_result = workon.JSONField('Google place Result', blank=True, null=True)

    class Meta:
        abstract = True