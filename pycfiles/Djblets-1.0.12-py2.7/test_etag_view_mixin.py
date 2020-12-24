# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/views/tests/test_etag_view_mixin.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for ETagViewMixin."""
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseNotModified
from django.test.client import RequestFactory
from django.views.generic.base import View
from djblets.testing.testcases import TestCase
from djblets.util.http import encode_etag
from djblets.views.generic.etag import ETagViewMixin

class ETagViewMixinTests(TestCase):
    """Unit tests for ETagViewMixin."""

    def test_get_with_matching_etag(self):
        """Testing ETagViewMixin.get with matching ETag"""
        self._test_with_matching_etag(b'GET')

    def test_get_without_matching_etag(self):
        """Testing ETagViewMixin.get without matching ETag"""
        self._test_without_matching_etag(b'GET')

    def test_head_with_matching_etag(self):
        """Testing ETagViewMixin.head with matching ETag"""
        self._test_with_matching_etag(b'HEAD')

    def test_head_without_matching_etag(self):
        """Testing ETagViewMixin.head without matching ETag"""
        self._test_without_matching_etag(b'HEAD')

    def test_post_ignores_etags(self):
        """Testing ETagViewMixin.post ignores ETags"""
        self._test_ignore_etag(b'POST')

    def test_put_ignores_etags(self):
        """Testing ETagViewMixin.put ignores ETags"""
        self._test_ignore_etag(b'PUT')

    def test_patch_ignores_etags(self):
        """Testing ETagViewMixin.patch ignores ETags"""
        self._test_ignore_etag(b'PATCH')

    def test_delete_ignores_etags(self):
        """Testing ETagViewMixin.delete ignores ETags"""
        self._test_ignore_etag(b'DELETE')

    def _test_with_matching_etag(self, method):

        class MyView(ETagViewMixin, View):

            def get_etag_data(self, *args, **kwargs):
                return b'test123'

        setattr(MyView, method.lower(), lambda *args, **kwargs: HttpResponse())
        view = MyView.as_view()
        request = RequestFactory().request(REQUEST_METHOD=b'HEAD')
        request.META[b'HTTP_IF_NONE_MATCH'] = encode_etag(b'test123')
        response = view(request)
        self.assertIsInstance(response, HttpResponseNotModified)
        self.assertFalse(response.has_header(b'ETag'))

    def _test_without_matching_etag(self, method):

        class MyView(ETagViewMixin, View):

            def get_etag_data(self, *args, **kwargs):
                return b'test123'

            def head(self, *args, **kwargs):
                return HttpResponse()

        setattr(MyView, method.lower(), lambda *args, **kwargs: HttpResponse())
        view = MyView.as_view()
        request = RequestFactory().request(REQUEST_METHOD=method)
        request.META[b'HTTP_IF_NONE_MATCH'] = encode_etag(b'nope')
        response = view(request)
        self.assertNotIsInstance(response, HttpResponseNotModified)
        self.assertTrue(response.has_header(b'ETag'))
        self.assertEqual(response[b'ETag'], encode_etag(b'test123'))

    def _test_ignore_etag(self, method):

        class MyView(ETagViewMixin, View):

            def get_etag_data(self, *args, **kwargs):
                return b'test123'

        setattr(MyView, method.lower(), lambda *args, **kwargs: HttpResponse(b'hi there'))
        view = MyView.as_view()
        request = RequestFactory().request(REQUEST_METHOD=method)
        request.META[b'HTTP_IF_NONE_MATCH'] = encode_etag(b'test123')
        response = view(request)
        self.assertNotIsInstance(response, HttpResponseNotModified)
        self.assertEqual(response.content, b'hi there')
        self.assertFalse(response.has_header(b'ETag'))