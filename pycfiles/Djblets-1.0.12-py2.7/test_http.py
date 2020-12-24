# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_http.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.http."""
from __future__ import unicode_literals
from django.http import HttpRequest
from djblets.testing.testcases import TestCase
from djblets.util.http import get_http_accept_lists, get_http_requested_mimetype, is_mimetype_a

class HttpTests(TestCase):
    """Unit tests for djblets.util.http."""

    def setUp(self):
        self.request = HttpRequest()
        self.request.META[b'HTTP_ACCEPT'] = b'application/json;q=0.5,application/xml,text/plain;q=0.0,*/*;q=0.0'

    def test_http_accept_lists(self):
        """Testing get_http_accept_lists"""
        acceptable_mimetypes, unacceptable_mimetypes = get_http_accept_lists(self.request)
        self.assertEqual(acceptable_mimetypes, [
         b'application/xml', b'application/json'])
        self.assertEqual(unacceptable_mimetypes, [b'text/plain', b'*/*'])

    def test_get_requested_mimetype_with_supported_mimetype(self):
        """Testing get_requested_mimetype with supported mimetype"""
        self.assertEqual(get_http_requested_mimetype(self.request, [b'foo/bar',
         b'application/json']), b'application/json')
        self.assertEqual(get_http_requested_mimetype(self.request, [b'application/xml']), b'application/xml')
        self.assertEqual(get_http_requested_mimetype(self.request, [b'application/json',
         b'application/xml']), b'application/xml')

    def test_get_requested_mimetype_with_no_consensus(self):
        """Testing get_requested_mimetype with no consensus between client and
        server
        """
        self.request.META[b'HTTP_ACCEPT'] = b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        self.assertEqual(get_http_requested_mimetype(self.request, [b'application/json',
         b'application/x-foo']), b'application/json')

    def test_get_requested_mimetype_with_wildcard_supported_mimetype(self):
        """Testing get_requested_mimetype with supported */* mimetype"""
        self.request.META[b'HTTP_ACCEPT'] = b'*/*'
        self.assertEqual(get_http_requested_mimetype(self.request, [b'application/json',
         b'application/xml']), b'application/json')

    def test_get_requested_mimetype_with_unsupported_mimetype(self):
        """Testing get_requested_mimetype with unsupported mimetype"""
        self.assertIsNone(get_http_requested_mimetype(self.request, [
         b'text/plain']))
        self.assertIsNone(get_http_requested_mimetype(self.request, [
         b'foo/bar']))

    def test_is_mimetype_a(self):
        """Testing is_mimetype_a"""
        self.assertTrue(is_mimetype_a(b'application/json', b'application/json'))
        self.assertTrue(is_mimetype_a(b'application/vnd.foo+json', b'application/json'))
        self.assertFalse(is_mimetype_a(b'application/xml', b'application/json'))
        self.assertFalse(is_mimetype_a(b'foo/vnd.bar+json', b'application/json'))