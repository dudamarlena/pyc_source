# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/tests/test_views.py
# Compiled at: 2018-01-09 13:54:21
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse
from banner.models import Banner

class DetailViewTestCase(TestCase):
    fixtures = [
     'sites.json']

    @classmethod
    def setUpTestData(cls):
        super(DetailViewTestCase, cls).setUpTestData()
        cls.banner = Banner.objects.create(title='Test Banner', style='BaseStyle')
        cls.banner.sites = Site.objects.all()
        cls.banner.publish()

    def test_view_renders(self):
        response = self.client.get(reverse('banner:banner-detail', args=[self.banner.slug]))
        self.assertEqual(response.status_code, 200)