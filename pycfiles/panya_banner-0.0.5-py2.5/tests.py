# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/banner/tests.py
# Compiled at: 2010-12-14 06:48:44
import unittest
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.sites.models import Site
from banner.templatetags import banner_inclusion_tags
from banner.models import Banner, BannerOption
from preferences import preferences
urlpatterns = patterns('', url('^some/path$', object, name='test_view_name'), url('^no/specified/banners$', object, name='no_specified_banners'))

class BannerInclusionTagsTestCase(unittest.TestCase):

    def test_resolve_banner(self):
        request = type('Request', (object,), {})
        request.urlconf = 'banner.tests'
        request.path = '/some/path'
        unpublished_banner = Banner()
        unpublished_banner.save()
        option = BannerOption(banner=unpublished_banner, banner_preferences=preferences.BannerPreferences, url_name='test_view_name', position='header')
        option.save()
        self.failIfEqual(unpublished_banner, banner_inclusion_tags.resolve_banner(request, 'header'))
        web_site = Site(domain='web.address.com')
        web_site.save()
        settings.SITE_ID = web_site.id
        published_banner = Banner(state='published')
        published_banner.save()
        published_banner.sites.add(web_site)
        option = BannerOption(banner=published_banner, banner_preferences=preferences.BannerPreferences, url_name='test_view_name', position='header')
        option.save()
        self.failUnlessEqual(published_banner, banner_inclusion_tags.resolve_banner(request, 'header'))
        self.failIfEqual(published_banner, banner_inclusion_tags.resolve_banner(request, 'bogus slot'))
        web_site = Site(domain='web.address.com')
        web_site.save()
        settings.SITE_ID = web_site.id
        published_banner2 = Banner(state='published')
        published_banner2.save()
        published_banner2.sites.add(web_site)
        option = BannerOption(banner=published_banner2, banner_preferences=preferences.BannerPreferences, url_name='test_view_name', url='/some/path', position='header')
        option.save()
        self.failIfEqual(published_banner2, banner_inclusion_tags.resolve_banner(request, 'header'))
        web_site = Site(domain='web.address.com')
        web_site.save()
        settings.SITE_ID = web_site.id
        published_banner3 = Banner(state='published')
        published_banner3.save()
        published_banner3.sites.add(web_site)
        option = BannerOption(banner=published_banner3, banner_preferences=preferences.BannerPreferences, url_name='test_view_name', position='header', is_default=True)
        option.save()
        request.path = '/no/specified/banners'
        self.failUnlessEqual(published_banner3, banner_inclusion_tags.resolve_banner(request, 'header'))