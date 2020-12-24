# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/tests/geoapp/feeds.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import absolute_import
from django.contrib.gis import feeds
from .models import City

class TestGeoRSS1(feeds.Feed):
    link = '/city/'
    title = 'Test GeoDjango Cities'

    def items(self):
        return City.objects.all()

    def item_link(self, item):
        return '/city/%s/' % item.pk

    def item_geometry(self, item):
        return item.point


class TestGeoRSS2(TestGeoRSS1):

    def geometry(self, obj):
        return (-123.3, -41.32, 174.78, 48.46)

    def item_geometry(self, item):
        return (
         item.point.x, item.point.y)


class TestGeoAtom1(TestGeoRSS1):
    feed_type = feeds.GeoAtom1Feed


class TestGeoAtom2(TestGeoRSS2):
    feed_type = feeds.GeoAtom1Feed

    def geometry(self, obj):
        return (
         (-123.3, -41.32), (174.78, 48.46))


class TestW3CGeo1(TestGeoRSS1):
    feed_type = feeds.W3CGeoFeed


class TestW3CGeo2(TestGeoRSS2):
    feed_type = feeds.W3CGeoFeed


class TestW3CGeo3(TestGeoRSS1):
    feed_type = feeds.W3CGeoFeed

    def item_geometry(self, item):
        from django.contrib.gis.geos import Polygon
        return Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))


feed_dict = {'rss1': TestGeoRSS1, 
   'rss2': TestGeoRSS2, 
   'atom1': TestGeoAtom1, 
   'atom2': TestGeoAtom2, 
   'w3cgeo1': TestW3CGeo1, 
   'w3cgeo2': TestW3CGeo2, 
   'w3cgeo3': TestW3CGeo3}