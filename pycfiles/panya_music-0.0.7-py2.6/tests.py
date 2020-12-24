# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/tests.py
# Compiled at: 2011-09-19 04:01:13
import unittest
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.query import QuerySet
from music.models import TrackContributor, Credit, Track
from music.views import ListenLive

class ListenLiveViewTestCase(unittest.TestCase):

    def test_get_queryset(self):
        queryset = ListenLive().get_queryset()
        self.failUnlessEqual(queryset.__class__, QuerySet)


class TrackTestCase(unittest.TestCase):

    def test_get_primary_contributors(self):
        web_site = Site(domain='web.address.com')
        web_site.save()
        settings.SITE_ID = web_site.id
        track = Track(title='title')
        track.save()
        contributor1 = TrackContributor(title='title', state='published')
        contributor1.save()
        contributor1.sites.add(web_site)
        contributor2 = TrackContributor(title='title', state='published')
        contributor2.save()
        contributor2.sites.add(web_site)
        contributor3 = TrackContributor(title='title', state='published')
        contributor3.save()
        contributor3.sites.add(web_site)
        contributor4 = TrackContributor(title='title', state='published')
        contributor4.save()
        contributor4.sites.add(web_site)
        unpublished_contributor = TrackContributor(title='title')
        unpublished_contributor.save()
        Credit(track=track, contributor=contributor1, role=2).save()
        Credit(track=track, contributor=contributor2, role=10).save()
        Credit(track=track, contributor=contributor3, role=2).save()
        Credit(track=track, contributor=unpublished_contributor, role=2).save()
        Credit(track=track, contributor=contributor4).save()
        primary_contributors = track.get_primary_contributors()
        self.failUnless(contributor1 in primary_contributors)
        self.failUnless(contributor3 in primary_contributors)
        self.failIf(contributor2 in primary_contributors)
        self.failIf(unpublished_contributor in primary_contributors)
        self.failIf(contributor4 in primary_contributors)