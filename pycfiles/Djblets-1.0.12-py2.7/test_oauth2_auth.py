# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_oauth2_auth.py
# Compiled at: 2019-06-12 01:17:17
"""Tests for OAuth2 authentication with the web API."""
from __future__ import unicode_literals
from datetime import timedelta
from django.conf.urls import include, url
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.utils import timezone
from oauth2_provider.models import AccessToken, Application
from djblets.webapi.auth.backends import reset_auth_backends
from djblets.webapi.auth.backends.oauth2_tokens import OAuth2TokenBackendMixin
from djblets.webapi.errors import LOGIN_FAILED, NOT_LOGGED_IN, OAUTH_ACCESS_DENIED_ERROR, OAUTH_MISSING_SCOPE_ERROR
from djblets.webapi.resources.mixins.oauth2_tokens import ResourceOAuth2TokenMixin
from djblets.webapi.testing.resources import make_resource_tree
from djblets.webapi.testing.testcases import TestCase, WebAPITestCaseMixin
resource_tree = make_resource_tree(mixins=[
 ResourceOAuth2TokenMixin], allow_anonymous_access=False)
root_resource = resource_tree.root_resource
urlpatterns = [
 url(b'^api/', include(root_resource.get_url_patterns()))]

class OAuth2ModelBackend(OAuth2TokenBackendMixin, ModelBackend):
    """An OAuth2-enabled backend for unit tests."""
    pass


class OAuth2TokenAuthTests(WebAPITestCaseMixin, TestCase):
    """Tests for OAuth2 token authentication."""
    SETTINGS = {b'AUTHENTICATION_BACKENDS': ('djblets.webapi.tests.test_oauth2_auth.OAuth2ModelBackend', ), 
       b'WEB_API_ROOT_RESOURCE': b'djblets.webapi.tests.test_oauth2_auth.root_resource', 
       b'WEB_API_AUTH_BACKENDS': ('djblets.webapi.auth.backends.oauth2_tokens.WebAPIOAuth2TokenAuthBackend', ), 
       b'ROOT_URLCONF': b'djblets.webapi.tests.test_oauth2_auth'}
    error_mimetype = b'application/json'

    @classmethod
    def setUpClass(cls):
        super(OAuth2TokenAuthTests, cls).setUpClass()
        reset_auth_backends()

    def tearDown(self):
        super(OAuth2TokenAuthTests, self).tearDown()
        reset_auth_backends()

    @override_settings(**SETTINGS)
    def setUp(self):
        super(OAuth2TokenAuthTests, self).setUp()
        self.owner = User.objects.create_user(username=b'app_owner', email=b'owner@example.com')
        self.application = Application.objects.create(name=b'Test Application', authorization_grant_type=Application.GRANT_IMPLICIT, redirect_uris=b'http://example.com/', user=self.owner)
        self.user = User.objects.create_user(username=b'app_user', email=b'user@example.com')

    @override_settings(**SETTINGS)
    def test_get(self):
        """Testing WebAPI OAuth2 token access with valid scope"""
        token = self._create_token(scope=b'root:read')
        rsp = self.api_get(b'/api/', expected_mimetype=b'application/json', HTTP_AUTHORIZATION=b'Bearer %s' % token.token)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')

    @override_settings(**SETTINGS)
    def test_get_unknown_scope(self):
        """Testing WebAPI OAuth2 token access with unknown scope"""
        token = self._create_token(scope=b'unknown')
        rsp = self.api_get(b'/api/', HTTP_AUTHORIZATION=b'Bearer %s' % token.token, expected_status=403)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'err', rsp)
        err = rsp[b'err']
        self.assertIn(b'code', err)
        self.assertEqual(err[b'code'], OAUTH_MISSING_SCOPE_ERROR.code)

    @override_settings(**SETTINGS)
    def test_get_scope_insufficient(self):
        """Testing WebAPI OAuth2 token access with insufficient scope"""
        token = self._create_token(scope=b'')
        rsp = self.api_get(b'/api/', HTTP_AUTHORIZATION=b'Bearer %s' % token.token, expected_status=403)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'err', rsp)
        err = rsp[b'err']
        self.assertIn(b'code', err)
        self.assertEqual(err[b'code'], OAUTH_MISSING_SCOPE_ERROR.code)

    @override_settings(**SETTINGS)
    def test_get_unallowed(self):
        """Testing WebAPI OAuth2 token access to a resource marked as
        inaccessible via OAuth2 tokens
        """
        token = self._create_token(scope=b'forbidden:read')
        rsp = self.api_get(b'/api/forbidden/', HTTP_AUTHORIZATION=b'Bearer %s' % token.token, expected_status=403)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'err', rsp)
        err = rsp[b'err']
        self.assertIn(b'code', err)
        self.assertEqual(err[b'code'], OAUTH_ACCESS_DENIED_ERROR.code)

    @override_settings(**SETTINGS)
    def test_get_expired(self):
        """Testing WebAPI OAuth2 token access with an expired token
        """
        token = self._create_token(scope=b'root:read', expires=timedelta(hours=-1))
        rsp = self.api_get(b'/api/', HTTP_AUTHORIZATION=b'Bearer %s' % token.token, expected_status=LOGIN_FAILED.http_status)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'err', rsp)
        err = rsp[b'err']
        self.assertIn(b'code', err)
        self.assertEqual(err[b'code'], LOGIN_FAILED.code)

    @override_settings(**SETTINGS)
    def test_get_session(self):
        """Testing WebAPI OAuth2 token access with a token stored in a session
        """
        token = self._create_token(scope=b'root:read')
        session_id = self._login_and_get_session(token)
        rsp = self.api_get(b'/api/', HTTP_COOKIE=b'sessionid=%s' % session_id, expected_mimetype=b'application/json')
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')

    @override_settings(**SETTINGS)
    def test_get_session_expired(self):
        """Testing WebAPI OAuth2 token access with an expired token stored in a
        session
        """
        token = self._create_token(scope=b'root:read')
        session_id = self._login_and_get_session(token)
        token.expires = timezone.now() - timedelta(hours=1)
        token.save(update_fields=('expires', ))
        rsp = self.api_get(b'/api/', HTTP_COOKIE=b'sessionid=%s' % session_id, expected_status=401)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'err', rsp)
        err = rsp[b'err']
        self.assertIn(b'code', err)
        self.assertEqual(err[b'code'], NOT_LOGGED_IN.code)

    @override_settings(**SETTINGS)
    def test_get_session_insufficient_scope(self):
        """Testing WebAPI OAuth2 token access with a token stored in a
        session with insufficient scope
        """
        token = self._create_token(scope=b'root:read')
        session_id = self._login_and_get_session(token)
        rsp = self.api_get(b'/api/parents/', HTTP_COOKIE=b'sessionid=%s' % session_id, expected_status=403)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'err', rsp)
        err = rsp[b'err']
        self.assertIn(b'code', err)
        self.assertEqual(err[b'code'], OAUTH_MISSING_SCOPE_ERROR.code)

    @override_settings(**SETTINGS)
    def test_get_session_token_access_forbidden(self):
        """Testing WebAPI OAuth2 token access with a token stored in a
        session against a resource not allowing token access
        """
        token = self._create_token(scope=b'root:read forbidden:read')
        session_id = self._login_and_get_session(token)
        rsp = self.api_get(b'/api/forbidden/', HTTP_COOKIE=b'sessionid=%s' % session_id, expected_status=403)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertIn(b'err', rsp)
        err = rsp[b'err']
        self.assertIn(b'code', err)
        self.assertEqual(err[b'code'], OAUTH_ACCESS_DENIED_ERROR.code)

    def _login_and_get_session(self, token):
        """Log in with a token and return the session ID.

        Args:
            token (oauth2_provider.models.AccessToken):
                The access token to log in with.

        Returns:
            unicode:
            The session ID.
        """
        rsp, result = self.api_get_with_response(b'/api/', HTTP_AUTHORIZATION=b'Bearer %s' % token.token, expected_mimetype=b'application/json')
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        return result.cookies[b'sessionid'].value

    def _create_token(self, scope, expires=None):
        """Create an OAuth2 access token for testing.

        Args:
            scope (unicode):
                The scopes of the token.

            expires (datetime.timedelta, optional):
                How far into the future the token expires. If not provided,
                this argument defaults to one hour.

        Returns:
            oauth2_provider.models.AccessToken:
            The created access token.
        """
        if expires is None:
            expires = timedelta(hours=1)
        return AccessToken.objects.create(user=self.user, token=b'oauth-token', application=self.application, expires=timezone.now() + expires, scope=scope)