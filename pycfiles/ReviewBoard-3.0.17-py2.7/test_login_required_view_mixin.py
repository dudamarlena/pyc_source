# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_login_required_view_mixin.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.mixins.LoginRequiredViewMixin."""
from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse, HttpResponseRedirect
from django.test.client import RequestFactory
from django.views.generic.base import View
from reviewboard.accounts.mixins import LoginRequiredViewMixin
from reviewboard.testing import TestCase

class LoginRequiredViewMixinTests(TestCase):
    """Unit tests for reviewboard.accounts.mixins.LoginRequiredViewMixin."""

    def test_dispatch_authenticated_user(self):
        """Testing LoginRequiredViewMixin.dispatch with authenticated user"""

        class MyView(LoginRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.assertTrue(view.request.user.is_authenticated())
                return HttpResponse(b'success')

        request = RequestFactory().request()
        request.user = User.objects.create_user(username=b'doc', email=b'doc@example.com')
        view = MyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_dispatch_anonymous_user(self):
        """Testing LoginRequiredViewMixin.dispatch with anonymous user"""

        class MyView(LoginRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.fail(b'Should not be reached')

        request = RequestFactory().request()
        request.user = AnonymousUser()
        view = MyView.as_view()
        response = view(request)
        self.assertIsInstance(response, HttpResponseRedirect)