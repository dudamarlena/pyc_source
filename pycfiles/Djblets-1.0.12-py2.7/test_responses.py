# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_responses.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import json
from django.test.client import RequestFactory
from djblets.testing.testcases import TestCase
from djblets.webapi.resources.registry import unregister_resource
from djblets.webapi.resources.user import UserResource

class WebAPIResponsePaginatedTests(TestCase):
    """Unit tests for djblets.webapi.responses.WebAPIResponsePaginated."""

    def setUp(self):
        super(WebAPIResponsePaginatedTests, self).setUp()
        self.factory = RequestFactory()
        self.user_resource = UserResource()

    def tearDown(self):
        super(WebAPIResponsePaginatedTests, self).tearDown()
        unregister_resource(self.user_resource)

    def test_pagination_serialization_encoding(self):
        """Testing WebAPIResponsePaginated query parameter encoding"""
        request = self.factory.get(b'/api/users/?q=%D0%B5')
        response = self.user_resource(request)
        rsp = json.loads(response.content)
        self.assertEqual(rsp[b'links'][b'self'][b'href'], b'http://testserver/api/users/?q=%D0%B5')