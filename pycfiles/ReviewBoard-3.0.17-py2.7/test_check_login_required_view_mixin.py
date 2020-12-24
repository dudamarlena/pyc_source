# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_check_login_required_view_mixin.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.mixins.CheckLoginRequiredViewMixin."""
from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse, HttpResponseRedirect
from django.test.client import RequestFactory
from django.views.generic.base import View
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.accounts.mixins import CheckLoginRequiredViewMixin
from reviewboard.testing import TestCase

class CheckLoginRequiredViewMixinTests(TestCase):
    """Unit tests for reviewboard.accounts.mixins.CheckLoginRequiredViewMixin.
    """

    def test_dispatch_authenticated_user(self):
        """Testing CheckLoginRequiredViewMixin.dispatch with authenticated user
        """

        class MyView(CheckLoginRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.assertTrue(view.request.user.is_authenticated())
                return HttpResponse(b'success')

        request = RequestFactory().request()
        request.user = User.objects.create_user(username=b'doc', email=b'doc@example.com')
        view = MyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_dispatch_anonymous_user_and_login_not_required(self):
        """Testing CheckLoginRequiredViewMixin.dispatch with anonymous user
        and login not required
        """

        class MyView(CheckLoginRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.assertTrue(view.request.user.is_anonymous())
                return HttpResponse(b'success')

        request = RequestFactory().request()
        request.user = AnonymousUser()
        with self.siteconfig_settings({b'auth_require_sitewide_login': False}, reload_settings=False):
            view = MyView.as_view()
            response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_dispatch_anonymous_user_and_login_required(self):
        """Testing CheckLoginRequiredViewMixin.dispatch with anonymous user
        and login required
        """

        class MyView(CheckLoginRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.assertTrue(view.request.user.is_anonymous())
                return HttpResponse(b'success')

        request = RequestFactory().request()
        request.user = AnonymousUser()
        with self.siteconfig_settings({b'auth_require_sitewide_login': True}, reload_settings=False):
            view = MyView.as_view()
            response = view(request)
        self.assertIsInstance(response, HttpResponseRedirect)