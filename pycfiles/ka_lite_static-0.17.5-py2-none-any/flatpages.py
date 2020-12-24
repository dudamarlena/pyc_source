# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/sitemaps/tests/flatpages.py
# Compiled at: 2018-07-11 18:15:31
from __future__ import unicode_literals
from django.conf import settings
from django.utils.unittest import skipUnless
from .base import SitemapTestsBase

class FlatpagesSitemapTests(SitemapTestsBase):

    @skipUnless(b'django.contrib.flatpages' in settings.INSTALLED_APPS, b'django.contrib.flatpages app not installed.')
    def test_flatpage_sitemap(self):
        """Basic FlatPage sitemap test"""
        from django.contrib.flatpages.models import FlatPage
        public = FlatPage.objects.create(url=b'/public/', title=b'Public Page', enable_comments=True, registration_required=False)
        public.sites.add(settings.SITE_ID)
        private = FlatPage.objects.create(url=b'/private/', title=b'Private Page', enable_comments=True, registration_required=True)
        private.sites.add(settings.SITE_ID)
        response = self.client.get(b'/flatpages/sitemap.xml')
        self.assertContains(response, b'<loc>%s%s</loc>' % (self.base_url, public.url))
        self.assertNotContains(response, b'<loc>%s%s</loc>' % (self.base_url, private.url))