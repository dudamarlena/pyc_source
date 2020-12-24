# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/john/pycharm_workspace/sop/unified_platform/libs/unified/shawty/tests.py
# Compiled at: 2012-11-12 17:59:56
"""
Contains all unit tests for django_shawty
"""
__author__ = 'john@unifiedsocial.com'
from django.test import TestCase
from django.core.cache import cache
from . import models
from django.conf import settings

class ShawtyTest(TestCase):

    def test_request_urls(self):
        long_urls = [
         'www.foo.com', 'www.bar.com', 'http://www.baz.com']
        output_dict = models.ShawtyURL.get_short_urls(long_urls)
        self.assertIn('http://www.foo.com', output_dict)
        self.assertIn('http://www.bar.com', output_dict)
        self.assertIn('http://www.baz.com', output_dict)
        if getattr(settings, models.SHAWTY_SETTING_USE_DB):
            models.ShawtyURL.objects.get(long_url='http://www.foo.com')
            models.ShawtyURL.objects.get(long_url='http://www.bar.com')
            models.ShawtyURL.objects.get(long_url='http://www.baz.com')
        if getattr(settings, models.SHAWTY_SETTING_USE_CACHE):
            self.assertIsNotNone(cache.get(models.SHAWTY_CACHE_KEY_PREFIX + 'http://www.foo.com'))
            self.assertIsNotNone(cache.get(models.SHAWTY_CACHE_KEY_PREFIX + 'http://www.bar.com'))
            self.assertIsNotNone(cache.get(models.SHAWTY_CACHE_KEY_PREFIX + 'http://www.baz.com'))
        long_urls = ['www.foo.com', 'www.bar.com', 'http://www.biz.com']
        output_dict = models.ShawtyURL.get_short_urls(long_urls)
        self.assertIn('http://www.foo.com', output_dict)
        self.assertIn('http://www.bar.com', output_dict)
        self.assertIn('http://www.biz.com', output_dict)
        if getattr(settings, models.SHAWTY_SETTING_USE_DB):
            models.ShawtyURL.objects.get(long_url='http://www.foo.com')
            models.ShawtyURL.objects.get(long_url='http://www.bar.com')
            models.ShawtyURL.objects.get(long_url='http://www.baz.com')
            models.ShawtyURL.objects.get(long_url='http://www.biz.com')
        if getattr(settings, models.SHAWTY_SETTING_USE_CACHE):
            self.assertIsNotNone(cache.get(models.SHAWTY_CACHE_KEY_PREFIX + 'http://www.foo.com'))
            self.assertIsNotNone(cache.get(models.SHAWTY_CACHE_KEY_PREFIX + 'http://www.bar.com'))
            self.assertIsNotNone(cache.get(models.SHAWTY_CACHE_KEY_PREFIX + 'http://www.baz.com'))
            self.assertIsNotNone(cache.get(models.SHAWTY_CACHE_KEY_PREFIX + 'http://www.biz.com'))