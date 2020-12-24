# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/auth/tests/test_ratelimit.py
# Compiled at: 2019-06-12 01:17:17
"""Tests for the utilities for rate-limiting login attempts."""
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory
from django.test.utils import override_settings
from django.utils import six
from djblets.auth.ratelimit import is_ratelimited, Rate
from djblets.testing.testcases import TestCase

class RateLimitTests(TestCase):
    """Unit tests for djblets.auth.ratelimit."""

    def setUp(self):
        super(RateLimitTests, self).setUp()
        self.request_factory = RequestFactory()

    def tearDown(self):
        super(RateLimitTests, self).tearDown()
        cache.clear()

    def test_rate_parsing(self):
        """Testing Rate.parse"""
        test_rates = (
         (
          b'100/s', Rate(100, 1)),
         (
          b'100/10s', Rate(100, 10)),
         (
          b'100/10', Rate(100, 10)),
         (
          b'100/m', Rate(100, 60)),
         (
          b'400/10m', Rate(400, 600)),
         (
          b'1000/h', Rate(1000, 3600)),
         (
          b'800/d', Rate(800, 86400)))
        for rate_str, rate in test_rates:
            self.assertEqual(rate, Rate.parse(rate_str))

    @override_settings(LOGIN_LIMIT_RATE=b'7/m')
    def test_unauthenticated_user(self):
        """Testing is_ratelimited with unauthenticated user"""
        request = self.request_factory.get(b'/')
        request.user = AnonymousUser()
        self.assertFalse(is_ratelimited(request, increment=False))

    @override_settings(LOGIN_LIMIT_RATE=b'blah')
    def test_invalid_rate_limit(self):
        """Testing is_ratelimited with invalid rate limit parameter"""
        request = self.request_factory.get(b'/')
        request.user = User(pk=1)
        with self.assertRaises(ImproperlyConfigured) as (context):
            is_ratelimited(request, increment=False)
        self.assertEqual(six.text_type(context.exception), b'LOGIN_LIMIT_RATE setting could not be parsed.')

    @override_settings(LOGIN_LIMIT_RATE=b'1/h')
    def test_rate_limit_exceeded(self):
        """Testing is_ratelimited when limit exceeded"""
        request = self.request_factory.get(b'/')
        request.user = User(pk=1)
        self.assertFalse(is_ratelimited(request, increment=True))
        self.assertTrue(is_ratelimited(request, increment=True))