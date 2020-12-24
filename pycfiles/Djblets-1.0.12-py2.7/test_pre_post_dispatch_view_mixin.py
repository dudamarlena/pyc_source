# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/views/tests/test_pre_post_dispatch_view_mixin.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for PrePostDispatchViewMixin."""
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseForbidden
from django.test.client import RequestFactory
from django.views.generic.base import View
from djblets.testing.testcases import TestCase
from djblets.views.generic.base import PrePostDispatchViewMixin

class PrePostDispatchViewMixinTests(TestCase):
    """Unit tests for PrePostDispatchViewMixin."""

    def test_dispatch(self):
        """Testing PrePostDispatchViewMixin.dispatch"""
        seen = set()

        class MyView(PrePostDispatchViewMixin, View):

            def pre_dispatch(self, *args, **kwargs):
                seen.add(b'pre_dispatch')

            def post_dispatch(self, response, *args, **kwargs):
                seen.add(b'post_dispatch')
                return response

        view = MyView.as_view()
        response = view(RequestFactory().request())
        self.assertEquals(seen, {b'pre_dispatch', b'post_dispatch'})
        self.assertIsInstance(response, HttpResponse)

    def test_dispatch_with_pre_dispatch_response(self):
        """Testing PrePostDispatchViewMixin.pre_dispatch with custom response
        """

        class MyView(PrePostDispatchViewMixin, View):

            def pre_dispatch(self, *args, **kwargs):
                return HttpResponseForbidden()

        view = MyView.as_view()
        response = view(RequestFactory().request())
        self.assertIsInstance(response, HttpResponseForbidden)

    def test_dispatch_with_post_dispatch_response(self):
        """Testing PrePostDispatchViewMixin.post_dispatch with custom response
        """

        class MyView(PrePostDispatchViewMixin, View):

            def post_dispatch(self, *args, **kwargs):
                return HttpResponseForbidden()

        view = MyView.as_view()
        response = view(RequestFactory().request())
        self.assertIsInstance(response, HttpResponseForbidden)