# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_api_auth_backend.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for the web API token auth backend."""
from __future__ import unicode_literals
import logging
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.cache import cache
from django.db import models
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils.translation import ugettext_lazy as _
from kgb import SpyAgency
from djblets.testing.testcases import TestCase, TestModelsLoaderMixin
from djblets.webapi.auth.backends.api_tokens import TokenAuthBackendMixin, WebAPITokenAuthBackend

class TestWebAPITokenModel(models.Model):
    """Mock WebAPI Token Model for testing purposes."""
    user = models.ForeignKey(User, related_name=b'webapi_tokens', on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)


class TestTokenAuthBackend(TokenAuthBackendMixin):
    """Mock Token Auth Backend for testing purposes."""
    api_token_model = TestWebAPITokenModel


@override_settings(AUTHENTICATION_BACKENDS=('djblets.webapi.tests.test_api_auth_backend.TestTokenAuthBackend', ))
class WebAPITokenAuthBackendTests(SpyAgency, TestModelsLoaderMixin, TestCase):
    """Unit tests for the WebAPITokenAuthBackend."""
    tests_app = b'djblets.webapi.tests'

    def setUp(self):
        super(WebAPITokenAuthBackendTests, self).setUp()
        self.api_token_auth_backend = WebAPITokenAuthBackend()
        self.request = RequestFactory().get(b'/')
        SessionMiddleware().process_request(self.request)

    def tearDown(self):
        super(WebAPITokenAuthBackendTests, self).tearDown()
        cache.clear()

    def test_get_credentials_no_token_realm(self):
        """Testing Token Auth get_credentials with non-token realm"""
        self.request.META[b'HTTP_AUTHORIZATION'] = b'NotTokenRealm tokenHere'
        result = self.api_token_auth_backend.get_credentials(self.request)
        self.assertIsNone(result)

    def test_get_credentials_missing_credentials(self):
        """Testing Token Auth get_credentials with missing token"""
        self.request.META[b'HTTP_AUTHORIZATION'] = b'token'
        logger = logging.getLogger(b'djblets.webapi.auth.backends.api_tokens')
        self.spy_on(logger.warning)
        result = self.api_token_auth_backend.get_credentials(self.request)
        self.assertIsNone(result)
        warning_message = logger.warning.spy.last_call.args[0]
        self.assertTrue(warning_message.startswith(b'WebAPITokenAuthBackend: Missing token in HTTP_AUTHORIZATION header'))

    def test_get_credentials_valid_credentials(self):
        """Testing Token Auth get_credentials with valid credentials"""
        token = b'myToken'
        self.request.META[b'HTTP_AUTHORIZATION'] = b'token %s' % token
        result = self.api_token_auth_backend.get_credentials(self.request)
        self.assertEqual(result, {b'token': token})

    def test_authenticate_valid_credentials(self):
        """Testing Token Auth authenticate succeeds"""
        token = b'invalidtoken123'
        self.user = User.objects.create_user(username=b'testuser')
        TestWebAPITokenModel.objects.create(user=self.user, token=token)
        self.request.user = User()
        self.request.META[b'HTTP_AUTHORIZATION'] = b'token %s' % token
        result = self.api_token_auth_backend.authenticate(self.request)
        self.assertEqual(result, (True, None, None))
        self.assertNotEqual(self.request.META[b'CSRF_COOKIE'], b'')
        return

    def test_authenticate_wrong_token(self):
        """Testing Token Auth authenticate failed with wrong token"""
        token = b'invalidtoken123'
        self.user = User.objects.create_user(username=b'testuser')
        TestWebAPITokenModel.objects.create(user=self.user, token=token)
        self.request.user = User()
        self.request.META[b'HTTP_AUTHORIZATION'] = b'token bad_token'
        result = self.api_token_auth_backend.authenticate(self.request)
        self.assertEqual(result, (False, None, None))
        return

    @override_settings(LOGIN_LIMIT_RATE=b'5/m')
    def test_authenticate_rate_limit(self):
        """Testing Token Auth authenticate failed and exceeding
        number of failed login attempts allowed with default rate limit
        """
        token = b'myToken'
        self.user = User.objects.create_user(username=b'testratelimit')
        TestWebAPITokenModel.objects.create(user=self.user, token=token)
        self.request.user = self.user
        self.request.META[b'HTTP_AUTHORIZATION'] = b'token bad_token'
        for i in range(5):
            result = self.api_token_auth_backend.authenticate(self.request)
            self.assertEqual(result, (False, None, None))

        result = self.api_token_auth_backend.authenticate(self.request)
        self.assertEqual(result, (
         False, _(b'Maximum number of login attempts exceeded.'), None))
        return

    @override_settings(LOGIN_LIMIT_RATE=b'3/s')
    def test_authenticate_custom_rate_limit_3_per_second(self):
        """Testing Token Auth authenticate failed and exceeding
        number of failed login attempts allowed with custom rate limit
        (3 failed attempts per second)
        """
        token = b'myRateLimitToken1'
        self.user = User.objects.create_user(username=b'testratelimit1')
        TestWebAPITokenModel.objects.create(user=self.user, token=token)
        self.request.user = self.user
        self.request.META[b'HTTP_AUTHORIZATION'] = b'token bad_token'
        for i in range(3):
            result = self.api_token_auth_backend.authenticate(self.request)
            self.assertEqual(result, (False, None, None))

        result = self.api_token_auth_backend.authenticate(self.request)
        self.assertEqual(result, (
         False, _(b'Maximum number of login attempts exceeded.'), None))
        return

    @override_settings(LOGIN_LIMIT_RATE=b'4/h')
    def test_authenticate_custom_rate_limit_4_per_hour(self):
        """Testing Token Auth authenticate failed and exceeding
        number of failed login attempts allowed with custom rate limit
        (4 failed attempts per hour)
        """
        token = b'myRateLimitToken2'
        self.user = User.objects.create_user(username=b'testratelimit2')
        TestWebAPITokenModel.objects.create(user=self.user, token=token)
        self.request.user = self.user
        self.request.META[b'HTTP_AUTHORIZATION'] = b'token bad_token'
        for i in range(4):
            result = self.api_token_auth_backend.authenticate(self.request)
            self.assertEqual(result, (False, None, None))

        result = self.api_token_auth_backend.authenticate(self.request)
        self.assertEqual(result, (
         False, _(b'Maximum number of login attempts exceeded.'), None))
        return