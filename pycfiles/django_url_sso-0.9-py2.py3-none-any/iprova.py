# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drbob/Development/hap-intra/env/src/django-url-sso/url_sso/tests/plugins/iprova.py
# Compiled at: 2014-02-10 05:24:48
import os
from mock import Mock, patch
from httmock import HTTMock
from django.core import cache
from django.test import TestCase
from django.test.utils import override_settings
from url_sso.plugins import iprova
from url_sso.plugins.iprova import iprova_plugin
from url_sso.tests.utils import RequestTestMixin, UserTestMixin
iprova_settings = {'root_url': 'http://intranet.organisation.com/', 
   'services': ('management', 'idocument', 'iportal', 'itask'), 
   'key_expiration': 3600, 
   'application_id': 'SharepointIntranet_Production'}
sso_settings = {'URL_SSO_PLUGINS': [
                     'url_sso.plugins.iprova.iprova_plugin'], 
   'URL_SSO_IPROVA': iprova_settings}

@override_settings(**sso_settings)
class iProvaTests(RequestTestMixin, UserTestMixin, TestCase):
    """ Tests for iProva SSO """
    test_token = '3f5c99f7d8214862afa8c27826b78e14'

    def setUp(self):
        self.locmem_cache = cache.get_cache('django.core.cache.backends.locmem.LocMemCache')
        self.locmem_cache.clear()
        self.cache_patch = patch.object(iprova, 'cache', self.locmem_cache)
        self.cache_patch.start()
        directory = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.test_wsdl = open(os.path.join(directory, 'iprova_usermanagement_wsdl.xml')).read()
        self.test_response = open(os.path.join(directory, 'iprova_token_response.xml')).read()
        super(iProvaTests, self).setUp()

    def tearDown(self):
        self.cache_patch.stop()

    def test_get_webservice(self):
        """ Use test WSDL to check whether or not SUDS is broken. """

        def wsdl_mock(url, request):
            self.assertEquals(url.geturl(), 'http://intranet.organisation.com/Management/Webservices/UserManagementAPI.asmx?WSDL')
            return self.test_wsdl

        with HTTMock(wsdl_mock):
            service = iprova_plugin._get_webservice()
        self.assertTrue(hasattr(service, 'GetTokenForUser'))
        with HTTMock(lambda url, request: self.test_response.format(token='test_token')):
            answer = service.GetTokenForUser(strTrustedApplicationID=iprova_settings['application_id'], strLoginCode='test_user')
        self.assertEquals(answer, 'test_token')

    def test_get_webservice_cache(self):
        """ Test caching for WSDL files """
        with HTTMock(lambda url, request: self.test_wsdl):
            service = iprova_plugin._get_webservice()
        with HTTMock(lambda url, request: self.fail('Expected one request.')):
            iprova_plugin._get_webservice()
        with HTTMock(lambda url, request: self.test_response.format(token='test_token_2')):
            answer = service.GetTokenForUser(strTrustedApplicationID=iprova_settings['application_id'], strLoginCode='test_user')
        self.assertEquals(answer, 'test_token_2')
        with HTTMock(lambda url, request: self.test_response.format(token='test_token_3')):
            answer = service.GetTokenForUser(strTrustedApplicationID=iprova_settings['application_id'], strLoginCode='test_user')
        self.assertEquals(answer, 'test_token_3')

    @patch('url_sso.plugins.iprova.iprova_plugin._get_webservice')
    def test_request_token(self, mock_method):
        """ Test _request_token() """
        mock_soap_call = Mock()

        class MockService(object):
            GetTokenForUser = mock_soap_call

        mock_soap_call.return_value = self.test_token
        mock_method.return_value = MockService
        token = iprova_plugin._request_token('test_user')
        mock_soap_call.assert_called_once_with(strTrustedApplicationID=iprova_settings['application_id'], strLoginCode='test_user')
        self.assertEquals(token, self.test_token)

    def test_get_cache_key(self):
        """ Test _get_cache_key() """
        cache_key = iprova_plugin._get_cache_key('my_name')
        self.assertEquals(cache_key, 'iprova_sso_my_name')

    @patch('url_sso.plugins.iprova.iprova_plugin._request_token')
    def test_get_login_token(self, mock_method):
        """ Test _get_login_token() """
        mock_method.return_value = self.test_token
        token = iprova_plugin._get_login_token('test_user')
        self.assertEquals(token, self.test_token)
        iprova_plugin._get_login_token('test_user')
        mock_method.assert_called_once_with('test_user')

    def test_generate_login_url(self):
        """ Test _generate_login_url() """
        login_url = iprova_plugin._generate_login_url('http://intranet.organisation.com/iprova/', self.test_token)
        self.assertEquals(login_url, 'http://intranet.organisation.com/iprova/?token=' + self.test_token)

    @patch('url_sso.plugins.iprova.iprova_plugin._get_login_token')
    def test_get_login_urls(self, mock_method):
        """ Test get_login_urls() """
        self.request.user = self.user
        mock_method.return_value = self.test_token
        urls = iprova_plugin.get_login_urls(self.request)
        self.assertEquals(urls, {'IPROVA_MANAGEMENT_SSO_URL': 'http://intranet.organisation.com/management/?token=' + self.test_token, 
           'IPROVA_IDOCUMENT_SSO_URL': 'http://intranet.organisation.com/idocument/?token=' + self.test_token, 
           'IPROVA_IPORTAL_SSO_URL': 'http://intranet.organisation.com/iportal/?token=' + self.test_token, 
           'IPROVA_ITASK_SSO_URL': 'http://intranet.organisation.com/itask/?token=' + self.test_token})
        mock_method.assert_called_once_with(self.user.username)

    @patch('url_sso.plugins.iprova.iprova_plugin._get_login_token')
    def test_has_access(self, mock_method):
        """ Test get_login_urls() with has_access = False """
        self.request.user = self.user
        mock_method.return_value = self.test_token
        local_settings = sso_settings.copy()
        local_settings['URL_SSO_IPROVA']['has_access'] = lambda request, service: False
        with override_settings(**local_settings):
            urls = iprova_plugin.get_login_urls(self.request)
        self.assertEquals(urls, {})
        self.assertFalse(mock_method.called)
        local_settings['URL_SSO_IPROVA']['has_access'] = lambda request, service: service == 'iportal'
        with override_settings(**local_settings):
            urls = iprova_plugin.get_login_urls(self.request)
        self.assertEquals(urls, {'IPROVA_IPORTAL_SSO_URL': 'http://intranet.organisation.com/iportal/?token=' + self.test_token})
        mock_method.assert_called_once_with(self.user.username)