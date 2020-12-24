# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_user_profile_required_view_mixin.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.mixins.UserProfileRequiredViewMixin."""
from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse
from django.test.client import RequestFactory
from django.views.generic.base import View
from reviewboard.accounts.mixins import UserProfileRequiredViewMixin
from reviewboard.accounts.models import Profile
from reviewboard.testing import TestCase

class UserProfileRequiredViewMixinTests(TestCase):
    """Unit tests for reviewboard.accounts.mixins.UserProfileRequiredViewMixin.
    """

    def test_dispatch_with_no_profile(self):
        """Testing UserProfileRequiredViewMixin.dispatch with authenticated
        user without a profile
        """

        class MyView(UserProfileRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.assertIsNotNone(view.request.user.get_profile())
                return HttpResponse(b'success')

        request = RequestFactory().request()
        request.user = User.objects.create_user(username=b'doc', email=b'doc@example.com')
        view = MyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_dispatch_with_profile(self):
        """Testing UserProfileRequiredViewMixin.dispatch with authenticated
        user with a profile
        """

        class MyView(UserProfileRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.assertIsNotNone(view.request.user.get_profile())
                return HttpResponse(b'success')

        request = RequestFactory().request()
        request.user = User.objects.create_user(username=b'doc', email=b'doc@example.com')
        Profile.objects.create(user=request.user)
        view = MyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_dispatch_with_anonymous(self):
        """Testing UserProfileRequiredViewMixin.dispatch with anonymous user"""

        class MyView(UserProfileRequiredViewMixin, View):

            def get(view, *args, **kwargs):
                self.assertIsInstance(view.request.user, AnonymousUser)
                return HttpResponse(b'success')

        request = RequestFactory().request()
        request.user = AnonymousUser()
        view = MyView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')