# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_api_ratelimit.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for API rate limiting."""
from __future__ import unicode_literals
import json
from django.test.utils import override_settings
from django.test.client import RequestFactory
from djblets.testing.testcases import TestCase
from djblets.webapi.errors import RATE_LIMIT_EXCEEDED
from djblets.webapi.resources.registry import unregister_resource
from djblets.webapi.resources.user import UserResource

class WebAPIRateLimitTests(TestCase):
    """Unit tests for API rate limiting."""

    def setUp(self):
        super(WebAPIRateLimitTests, self).setUp()
        self.factory = RequestFactory()
        self.user_resource = UserResource()

    def tearDown(self):
        super(WebAPIRateLimitTests, self).tearDown()
        unregister_resource(self.user_resource)

    @override_settings(API_ANONYMOUS_LIMIT_RATE=b'2/h')
    def test_api_rate_limit(self):
        """Testing API rate limiting."""
        request = self.factory.get(b'/api/')
        response = self.user_resource(request)
        self.assertEqual(response.status_code, 200)
        response = self.user_resource(request)
        self.assertEqual(response.status_code, 200)
        response = self.user_resource(request)
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response[b'X-RateLimit-Limit'], b'2')
        rsp = json.loads(response.content)
        self.assertEqual(rsp[b'err'][b'code'], RATE_LIMIT_EXCEEDED.code)