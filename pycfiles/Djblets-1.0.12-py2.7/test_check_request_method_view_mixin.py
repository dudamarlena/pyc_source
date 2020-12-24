# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/views/tests/test_check_request_method_view_mixin.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for CheckRequestMethodViewMixin."""
from __future__ import unicode_literals
from django.http import HttpResponse
from django.test.client import RequestFactory
from django.views.generic.base import View
from djblets.testing.testcases import TestCase
from djblets.views.generic.base import CheckRequestMethodViewMixin

class BaseTestView(View):

    def dispatch(self, request, *args, **kwargs):
        return getattr(self, request.method.lower())(request, *args, **kwargs)


class CheckRequestMethodViewMixinTests(TestCase):
    """Unit tests for CheckRequestMethodViewMixin."""

    def test_dispatch_with_allowed(self):
        """Testing CheckRequestMethodViewMixin.dispatch with HTTP method
        allowed
        """

        class MyView(CheckRequestMethodViewMixin, BaseTestView):

            def get(self, *args, **kwargs):
                return HttpResponse(b'ok')

        view = MyView.as_view()
        response = view(RequestFactory().request())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'ok')

    def test_dispatch_with_not_allowed(self):
        """Testing CheckRequestMethodViewMixin.dispatch with HTTP method
        not allowed
        """

        class MyView(CheckRequestMethodViewMixin, BaseTestView):

            def get(self, *args, **kwargs):
                return HttpResponse(b'ok')

        view = MyView.as_view()
        response = view(RequestFactory().request(REQUEST_METHOD=b'POST'))
        self.assertEqual(response.status_code, 405)
        self.assertNotEqual(response.content, b'ok')