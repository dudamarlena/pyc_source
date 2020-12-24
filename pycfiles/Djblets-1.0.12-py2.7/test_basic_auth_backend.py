# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/tests/test_basic_auth_backend.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for the web API basic auth backend."""
from __future__ import unicode_literals
import base64, logging
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from kgb import SpyAgency
from djblets.testing.testcases import TestCase
from djblets.webapi.auth.backends.basic import WebAPIBasicAuthBackend

class WebAPIBasicAuthBackendTests(SpyAgency, TestCase):
    """Unit tests for the WebAPIBasicAuthBackend."""

    def setUp(self):
        super(WebAPIBasicAuthBackendTests, self).setUp()
        self.basic_auth_backend = WebAPIBasicAuthBackend()
        self.request = RequestFactory().get(b'/')
        SessionMiddleware().process_request(self.request)
        self.request.user = AnonymousUser()
        self.user = User.objects.create_user(username=b'testuser', email=b'testcase@test.com', password=b'testpassword')

    def test_get_credentials_no_basic_realm(self):
        """Testing Basic Auth get_credentials with non-basic realm"""
        self.request.META[b'HTTP_AUTHORIZATION'] = b'Token tokenHere'
        result = self.basic_auth_backend.get_credentials(self.request)
        self.assertIsNone(result)

    def test_get_credentials_valid_credentials(self):
        """Testing Basic Auth get_credentials with credentials"""
        username = b'username'
        password = b'password'
        encoded_credentials = base64.b64encode(b'%s:%s' % (username, password))
        header = b'Basic ' + encoded_credentials
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        result = self.basic_auth_backend.get_credentials(self.request)
        self.assertEqual(result, {b'username': username, 
           b'password': password})

    def test_get_credentials_malformed_credentials(self):
        """Testing Basic Auth get_credentials with malformed credentials"""
        header = b'Basic ' + base64.b64encode(b'Some malfomred credentials')
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        logger = logging.getLogger(b'djblets.webapi.auth.backends.basic')
        self.spy_on(logger.warning)
        result = self.basic_auth_backend.get_credentials(self.request)
        warning_message = logger.warning.spy.last_call.args[0]
        self.assertIsNone(result)
        self.assertTrue(warning_message.startswith(b'Failed to parse HTTP_AUTHORIZATION header'))

    def test_authenticate_valid_credentials(self):
        """Testing Basic Auth authenicate with valid credentials"""
        credentials = b'%s:%s' % ('testuser', 'testpassword')
        header = b'Basic ' + base64.b64encode(credentials)
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        result = self.basic_auth_backend.authenticate(self.request)
        self.assertEqual(result, (True, None, None))
        return

    def test_authenticate_wrong_header(self):
        """Testing Basic Auth authenicate with wrong header"""
        credentials = b'%s:%s' % ('testuser', 'testpassword')
        header = b'Token ' + base64.b64encode(credentials)
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        result = self.basic_auth_backend.authenticate(self.request)
        self.assertIsNone(result)

    def test_authenticate_wrong_password(self):
        """Testing Basic Auth authenicate with invalid credentials"""
        credentials = b'%s:%s' % ('testuser', 'wrongpassword')
        header = b'Basic ' + base64.b64encode(credentials)
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        result = self.basic_auth_backend.authenticate(self.request)
        self.assertEqual(result, (False, None, None))
        return

    def test_login_with_credentials_valid_credentials(self):
        """Testing Basic Auth login_with_credentials with valid credentials"""
        username = b'testuser'
        password = b'testpassword'
        encoded_credentials = base64.b64encode(b'%s:%s' % (username, password))
        header = b'Basic ' + encoded_credentials
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        result = self.basic_auth_backend.login_with_credentials(self.request, username=username, password=password)
        self.assertEqual(result, (True, None, None))
        return

    def test_login_bypass_authentication(self):
        """Testing Basic Auth login_with_credentials with currently logged in
        user"""
        username = b'testuser'
        password = b'testpassword'
        encoded_credentials = base64.b64encode(b'%s:%s' % (username, password))
        header = b'Basic ' + encoded_credentials
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        self.request.user = self.user
        result = self.basic_auth_backend.login_with_credentials(self.request, username=username, password=password)
        self.assertEqual(result, (True, None, None))
        return

    def test_login_with_credentials_incorrect_pass(self):
        """Testing Basic Auth login_with_credentials with incorrect password"""
        username = b'testuser'
        password = b'wrongpassword'
        encoded_credentials = base64.b64encode(b'%s:%s' % (username, password))
        header = b'Basic ' + encoded_credentials
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        result = self.basic_auth_backend.login_with_credentials(self.request, username=username, password=password)
        self.assertEqual(result, (False, None, None))
        return

    def test_login_with_credentials_incorrect_user(self):
        """Testing Basic Auth login_with_credentials with invalid user"""
        username = b'wronguser'
        password = b'testpassword'
        encoded_credentials = base64.b64encode(b'%s:%s' % (username, password))
        header = b'Basic ' + encoded_credentials
        self.request.META[b'HTTP_AUTHORIZATION'] = header
        self.request.user = self.user
        result = self.basic_auth_backend.login_with_credentials(self.request, username=username, password=password)
        self.assertEqual(result, (False, None, None))
        return

    def test_validate_credentials_valid(self):
        """Testing Basic Auth validate_credentials with valid credentials"""
        self.request.user = self.user
        result = self.basic_auth_backend.validate_credentials(self.request, username=b'testuser', password=b'testpassword')
        self.assertEqual(result, (True, None, None))
        return

    def test_validate_credentials_invalid_user(self):
        """Testing Basic Auth validate_credentials with invalid user"""
        result = self.basic_auth_backend.validate_credentials(self.request, username=b'testuser', password=b'testpassword')
        self.assertIsNone(result)

    def test_validate_credentials_invalid_credentials(self):
        """Testing Basic Auth validate_credentials with invalid credentials"""
        self.request.user = self.user
        result = self.basic_auth_backend.validate_credentials(self.request, username=b'differentuser', password=b'testpassword')
        self.assertIsNone(result)

    def test_clean_credentials_for_display_removes_credentials(self):
        """Testing Basic Auth clean_credentials_for_display"""
        credentials = {b'api': b'has exact match', 
           b'oauth2_token': b'has partial match', 
           b'apikey2': b'no match as word but contains match sub string', 
           b'secre': b'no match, similar only'}
        removed_credential = b'************'
        clean_credentials = self.basic_auth_backend.clean_credentials_for_display(credentials)
        self.assertEqual(clean_credentials[b'api'], removed_credential)
        self.assertEqual(clean_credentials[b'oauth2_token'], removed_credential)
        self.assertEqual(clean_credentials[b'apikey2'], removed_credential)
        self.assertEqual(clean_credentials[b'secre'], credentials[b'secre'])