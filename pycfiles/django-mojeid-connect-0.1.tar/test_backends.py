# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: django_mojeid_connect/tests/test_backends.py
# Compiled at: 2018-07-09 08:45:07
"""Unittests for backends."""
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.cache import SessionStore
from django.test import RequestFactory, TestCase, override_settings
from django_oidc_sub.models import OidcUserSub
from django_mojeid_connect.backends import MojeidOidcBackend

@override_settings(OIDC_OP_AUTHORIZATION_ENDPOINT=b'http://example/oidc/authorization', OIDC_OP_TOKEN_ENDPOINT=b'http://example/oidc/token', OIDC_OP_USER_ENDPOINT=b'http://example/oidc/user', OIDC_RP_CLIENT_ID=b'clientid', OIDC_RP_CLIENT_SECRET=b'client_secret')
class TestMojeidOidcBackend(TestCase):
    """Unittests for MojeidOidcBackend."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username=b'test')
        request = RequestFactory().get(b'/')
        request.session = SessionStore()
        request.user = AnonymousUser()
        cls.backend = MojeidOidcBackend()
        cls.backend.request = request

    def test_no_user(self):
        queryset = self.backend.filter_users_by_claims({b'sub': b'aaa'})
        self.assertQuerysetEqual(queryset.values_list(b'username'), [], transform=tuple)

    def test_match_sub(self):
        OidcUserSub.objects.create(user=self.user, sub=b'aaa')
        queryset = self.backend.filter_users_by_claims({b'sub': b'aaa'})
        self.assertQuerysetEqual(queryset.values_list(b'username'), [('test', )], transform=tuple)

    def test_pairing(self):
        self.backend.request.user = self.user
        queryset = self.backend.filter_users_by_claims({b'sub': b'aaa'})
        self.assertQuerysetEqual(queryset.values_list(b'username'), [('test', )], transform=tuple)
        self.assertQuerysetEqual(OidcUserSub.objects.filter(sub=b'aaa').values_list(b'user__username'), [
         ('test', )], transform=tuple)