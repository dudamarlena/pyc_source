# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/tests/geoapp/sitemaps.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import absolute_import
from django.contrib.gis.sitemaps import GeoRSSSitemap, KMLSitemap, KMZSitemap
from .feeds import feed_dict
from .models import City, Country
sitemaps = {'kml': KMLSitemap([City, Country]), 'kmz': KMZSitemap([City, Country]), 
   'georss': GeoRSSSitemap(feed_dict)}