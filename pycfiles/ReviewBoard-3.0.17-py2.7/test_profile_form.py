# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_profile_form.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.accounts.forms.pages.ProfileForm."""
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from kgb import SpyAgency
from reviewboard.accounts.backends import AuthBackend, get_enabled_auth_backends
from reviewboard.accounts.forms.pages import ProfileForm
from reviewboard.accounts.models import Profile
from reviewboard.testing import TestCase

class SandboxAuthBackend(AuthBackend):
    """Mock authentication backend to test extension sandboxing."""
    backend_id = b'test-id'
    name = b'test'
    supports_change_name = True
    supports_change_email = True

    def update_name(self, user):
        """Raise an exception to test sandboxing."""
        raise Exception

    def update_email(self, user):
        """Raise an exception to test sandboxing."""
        raise Exception


class ProfileFormTests(SpyAgency, TestCase):
    """Unit tests for reviewboard.accounts.forms.pages.ProfileForm."""

    def setUp(self):
        super(ProfileFormTests, self).setUp()
        self.factory = RequestFactory()
        self.request = self.factory.get(b'test')
        self.user = User.objects.create_user(username=b'reviewboard', email=b'', password=b'password')
        self.profile = self.user.get_profile()
        self.spy_on(get_enabled_auth_backends, call_fake=lambda : [
         SandboxAuthBackend()])
        self.spy_on(messages.add_message, call_fake=lambda *args, **kwargs: None)

    def test_update_name_auth_backend(self):
        """Testing ProfileForm.save with error in auth_backend.update_name"""
        form = ProfileForm(page=None, request=self.request, user=self.user)
        form.cleaned_data = {b'first_name': b'Barry', 
           b'last_name': b'Allen', 
           b'email': b'flash@example.com', 
           b'profile_private': b''}
        self.user.email = b'flash@example.com'
        self.spy_on(SandboxAuthBackend.update_name)
        form.save()
        self.assertTrue(SandboxAuthBackend.update_name.called)
        return

    def test_update_email_auth_backend(self):
        """Testing ProfileForm.save with error in auth_backend.update_email"""
        form = ProfileForm(page=None, request=self.request, user=self.user)
        form.cleaned_data = {b'first_name': b'Barry', 
           b'last_name': b'Allen', 
           b'email': b'flash@example.com', 
           b'profile_private': b''}
        self.user.first_name = b'Barry'
        self.user.last_name = b'Allen'
        self.spy_on(SandboxAuthBackend.update_email)
        form.save()
        self.assertTrue(SandboxAuthBackend.update_email.called)
        return