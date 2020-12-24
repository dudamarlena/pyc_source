# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/urls/tests.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import warnings, django
from django.conf.urls import include, url
from django.core.urlresolvers import NoReverseMatch, clear_url_caches, reverse
from django.utils import six
from django.views.decorators.cache import never_cache
from kgb import SpyAgency
from djblets.testing.testcases import TestCase
from djblets.urls.patterns import never_cache_patterns
from djblets.urls.resolvers import DynamicURLResolver

def dummy_view(request):
    pass


class URLPatternsTests(SpyAgency, TestCase):
    """Unit tests for djblets.urls.patterns."""

    def test_never_cache_patterns_with_prefix(self):
        """Testing never_cache_patterns with view lookup string prefix"""
        msg = b'String prefixes for URLs in never_cache_patterns() is deprecated, and will not work on Django 1.10 or higher.'
        if django.VERSION[:2] >= (1, 10):
            with self.assertRaisesMessage(ValueError, msg):
                never_cache_patterns(b'djblets.urls.tests', url(b'^a/$', dummy_view))
        else:
            self.spy_on(never_cache)
            with warnings.catch_warnings(record=True) as (w):
                urlpatterns = never_cache_patterns(b'djblets.urls.tests', url(b'^a/$', b'dummy_view'), url(b'^b/$', b'dummy_view'))
            self.assertEqual(six.text_type(w[(-1)].message), msg)
            self.assertEqual(len(never_cache.spy.calls), 2)
            self.assertEqual(len(urlpatterns), 2)
            pattern = urlpatterns[0]
            self.assertEqual(pattern._callback_str, b'djblets.urls.tests.dummy_view')
            self.assertTrue(never_cache.spy.calls[0].returned(pattern.callback))
            pattern = urlpatterns[1]
            self.assertEqual(pattern._callback_str, b'djblets.urls.tests.dummy_view')
            self.assertTrue(never_cache.spy.calls[1].returned(pattern.callback))

    def test_never_cache_patterns_without_prefix(self):
        """Testing never_cache_patterns without view lookup string prefix"""
        self.spy_on(never_cache)
        with warnings.catch_warnings(record=True) as (w):
            urlpatterns = never_cache_patterns(url(b'^a/$', dummy_view), url(b'^b/$', dummy_view))
        self.assertEqual(len(w), 0)
        self.assertEqual(len(never_cache.spy.calls), 2)
        self.assertEqual(len(urlpatterns), 2)
        self.assertTrue(never_cache.spy.calls[0].returned(urlpatterns[0].callback))
        self.assertTrue(never_cache.spy.calls[1].returned(urlpatterns[1].callback))


class URLResolverTests(TestCase):

    def tearDown(self):
        super(URLResolverTests, self).tearDown()
        clear_url_caches()

    def test_dynamic_url_resolver(self):
        """Testing DynamicURLResolver"""

        def dummy_view(self):
            pass

        dynamic_urls = DynamicURLResolver()
        root_urlconf = [
         url(b'^root/', include([dynamic_urls])),
         url(b'^foo/', dummy_view, name=b'foo')]
        with self.settings(ROOT_URLCONF=root_urlconf):
            clear_url_caches()
            new_patterns = [
             url(b'^bar/$', dummy_view, name=b'bar'),
             url(b'^baz/$', dummy_view, name=b'baz')]
            reverse(b'foo')
            self.assertRaises(NoReverseMatch, reverse, b'bar')
            self.assertRaises(NoReverseMatch, reverse, b'baz')
            dynamic_urls.add_patterns(new_patterns)
            reverse(b'foo')
            reverse(b'bar')
            reverse(b'baz')
            dynamic_urls.remove_patterns(new_patterns)
            reverse(b'foo')
            self.assertRaises(NoReverseMatch, reverse, b'bar')
            self.assertRaises(NoReverseMatch, reverse, b'baz')