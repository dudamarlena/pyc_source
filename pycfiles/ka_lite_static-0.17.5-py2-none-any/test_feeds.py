# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/tests/geoapp/test_feeds.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import absolute_import
from xml.dom import minidom
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase
from .models import City

class GeoFeedTest(TestCase):
    urls = 'django.contrib.gis.tests.geoapp.urls'

    def setUp(self):
        Site(id=settings.SITE_ID, domain='example.com', name='example.com').save()
        self.old_Site_meta_installed = Site._meta.installed
        Site._meta.installed = True

    def tearDown(self):
        Site._meta.installed = self.old_Site_meta_installed

    def assertChildNodes(self, elem, expected):
        """Taken from regressiontests/syndication/tests.py."""
        actual = set([ n.nodeName for n in elem.childNodes ])
        expected = set(expected)
        self.assertEqual(actual, expected)

    def test_geofeed_rss(self):
        """Tests geographic feeds using GeoRSS over RSSv2."""
        doc1 = minidom.parseString(self.client.get('/feeds/rss1/').content)
        doc2 = minidom.parseString(self.client.get('/feeds/rss2/').content)
        feed1, feed2 = doc1.firstChild, doc2.firstChild
        self.assertChildNodes(feed2.getElementsByTagName('channel')[0], [
         'title', 'link', 'description', 'language',
         'lastBuildDate', 'item', 'georss:box', 'atom:link'])
        for feed in [feed1, feed2]:
            self.assertEqual(feed.getAttribute('xmlns:georss'), 'http://www.georss.org/georss')
            chan = feed.getElementsByTagName('channel')[0]
            items = chan.getElementsByTagName('item')
            self.assertEqual(len(items), City.objects.count())
            for item in items:
                self.assertChildNodes(item, ['title', 'link', 'description', 'guid', 'georss:point'])

    def test_geofeed_atom(self):
        """Testing geographic feeds using GeoRSS over Atom."""
        doc1 = minidom.parseString(self.client.get('/feeds/atom1/').content)
        doc2 = minidom.parseString(self.client.get('/feeds/atom2/').content)
        feed1, feed2 = doc1.firstChild, doc2.firstChild
        self.assertChildNodes(feed2, ['title', 'link', 'id', 'updated', 'entry', 'georss:box'])
        for feed in [feed1, feed2]:
            self.assertEqual(feed.getAttribute('xmlns:georss'), 'http://www.georss.org/georss')
            entries = feed.getElementsByTagName('entry')
            self.assertEqual(len(entries), City.objects.count())
            for entry in entries:
                self.assertChildNodes(entry, ['title', 'link', 'id', 'summary', 'georss:point'])

    def test_geofeed_w3c(self):
        """Testing geographic feeds using W3C Geo."""
        doc = minidom.parseString(self.client.get('/feeds/w3cgeo1/').content)
        feed = doc.firstChild
        self.assertEqual(feed.getAttribute('xmlns:geo'), 'http://www.w3.org/2003/01/geo/wgs84_pos#')
        chan = feed.getElementsByTagName('channel')[0]
        items = chan.getElementsByTagName('item')
        self.assertEqual(len(items), City.objects.count())
        for item in items:
            self.assertChildNodes(item, ['title', 'link', 'description', 'guid', 'geo:lat', 'geo:lon'])

        self.assertRaises(ValueError, self.client.get, '/feeds/w3cgeo2/')
        self.assertRaises(ValueError, self.client.get, '/feeds/w3cgeo3/')