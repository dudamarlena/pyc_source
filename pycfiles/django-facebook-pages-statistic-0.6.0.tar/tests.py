# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-facebook-pages-statistic/facebook_pages_statistic/tests.py
# Compiled at: 2015-03-06 07:16:08
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from facebook_api.signals import facebook_api_post_fetch
from facebook_pages.factories import PageFactory
from facebook_pages.models import Page
from models import PageStatistic
PAGE_FANS_ID = 19292868552

class FacebookPagesStatisticTest(TestCase):

    def test_page_statistic_create(self):
        self.assertEqual(PageStatistic.objects.count(), 0)
        page = PageFactory(graph_id=PAGE_FANS_ID, likes_count=10, talking_about_count=20)
        self.assertEqual(PageStatistic.objects.count(), 0)
        facebook_api_post_fetch.send(sender=page.__class__, instance=page, created=True)
        self.assertEqual(PageStatistic.objects.count(), 1)
        stat = page.statistics.latest()
        self.assertEqual(stat.likes_count, 10)
        self.assertEqual(stat.talking_about_count, 20)
        self.assertTrue(isinstance(stat.updated_at, datetime))
        page = Page.remote.fetch(PAGE_FANS_ID)
        self.assertEqual(PageStatistic.objects.count(), 2)
        stat = page.statistics.latest()
        self.assertTrue(stat.likes_count > 10)
        self.assertTrue(stat.talking_about_count > 20)
        self.assertTrue(isinstance(stat.updated_at, datetime))

    def test_null_stats_test(self):
        page = PageFactory(likes_count=None, talking_about_count=None)
        facebook_api_post_fetch.send(sender=page.__class__, instance=page, created=True)
        self.assertEqual(PageStatistic.objects.count(), 0)
        return