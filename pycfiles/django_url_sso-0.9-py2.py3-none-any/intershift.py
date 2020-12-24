# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drbob/Development/hap-intra/env/src/django-url-sso/url_sso/tests/plugins/intershift.py
# Compiled at: 2014-02-06 12:00:33
from mock import patch
from httmock import urlmatch, HTTMock
from django.core import cache
from django.test import TestCase
from django.test.utils import override_settings
from url_sso.context_processors import login_urls
from url_sso.tests.utils import RequestTestMixin, UserTestMixin
from url_sso.exceptions import RequestKeyException
from url_sso.plugins import intershift
from url_sso.plugins.intershift import intershift_plugin
intershift_settings = {'secret': '12345678', 
   'sites': {'site1': {'has_access': lambda request: False, 
                       'url': 'https://customer1.intershift.nl/site1/cust/singlesignon.asp'}, 
             'site2': {'has_access': lambda request: True, 
                       'url': 'https://customer1.intershift.nl/site2/cust/singlesignon.asp'}, 
             'site3': {'url': 'https://customer1.intershift.nl/site3/cust/singlesignon.asp'}}, 
   'key_expiration': 86400}
sso_settings = {'URL_SSO_PLUGINS': [
                     'url_sso.plugins.intershift.intershift_plugin'], 
   'URL_SSO_INTERSHIFT': intershift_settings}

@override_settings(**sso_settings)
class IntershiftTests(RequestTestMixin, UserTestMixin, TestCase):
    """ Tests for Intershift SSO. """
    test_key = 'BOGUSKEY'
    test_xml = '<?XML VERSION="1.0" Encoding="UTF-8"?><xml><key value="BOGUSKEY" /></xml>'
    test_login_url = 'https://customer1.intershift.nl/site1/cust/singlesignon.asp?user=john&key=BOGUSKEY'
    test_login_urls = {'INTERSHIFT_SITE2_SSO_URL': 'https://customer1.intershift.nl/site2/cust/singlesignon.asp?user=john&key=BOGUSKEY', 
       'INTERSHIFT_SITE3_SSO_URL': 'https://customer1.intershift.nl/site3/cust/singlesignon.asp?user=john&key=BOGUSKEY'}

    def setUp(self):
        self.locmem_cache = cache.get_cache('django.core.cache.backends.locmem.LocMemCache')
        self.locmem_cache.clear()
        self.cache_patch = patch.object(intershift, 'cache', self.locmem_cache)
        self.cache_patch.start()
        super(IntershiftTests, self).setUp()

    def tearDown(self):
        self.cache_patch.stop()

    def test_get_site_url(self):
        """ Test _get_site_url() """
        site_url = intershift_plugin._get_site_url('site1')
        self.assertEquals(site_url, intershift_settings['sites']['site1']['url'])

    def test_parse_login_key(self):
        """ Test _parse_login_key() """
        login_key = intershift_plugin._parse_login_key(self.test_xml)
        self.assertEquals(login_key, self.test_key)

    def test_parse_login_key_exceptions(self):
        """ Test for exception on invalid key """
        invalid_xml = 'banana'
        self.assertRaises(RequestKeyException, lambda : intershift_plugin._parse_login_key(invalid_xml))
        empty_key = '<?XML VERSION="1.0" Encoding="UTF-8"?><xml><key value="" /></xml>'
        self.assertRaises(RequestKeyException, lambda : intershift_plugin._parse_login_key(empty_key))

    def test_request_login_key(self):
        """ Test _request_login_key() """

        @urlmatch(scheme='https', netloc='customer1.intershift.nl', path='/site1/cust/singlesignon.asp')
        def key_mock(url, request):
            return self.test_xml

        with HTTMock(key_mock):
            login_key = intershift_plugin._request_login_key(site_name='site1', username=self.user.username)
        self.assertEquals(login_key, self.test_key)

    def test_request_login_500(self):
        """ Test exceptions on 500 in _request_login_key() """

        def mock_servererror(url, request):
            return {'status_code': 500}

        with HTTMock(mock_servererror):
            self.assertRaises(RequestKeyException, lambda : intershift_plugin._request_login_key('site1', self.user.username))

    def test_request_login_empty(self):
        """ Test exception on empty answer from _request_login_key() """

        def mock_empty(url, request):
            return ''

        with HTTMock(mock_empty):
            self.assertRaises(RequestKeyException, lambda : intershift_plugin._request_login_key('site1', self.user.username))

    def test_generate_login_url(self):
        """ Test _generate_login_url() """

        def key_mock(url, request):
            return self.test_xml

        with HTTMock(key_mock):
            login_url = intershift_plugin._generate_login_url('site1', self.user.username)
        self.assertEquals(login_url, self.test_login_url)

    def test_generate_login_url_cache(self):
        """ Test caching for _generate_login_url() """

        def key_mock(url, request):
            return self.test_xml

        with HTTMock(key_mock):
            intershift_plugin._generate_login_url('site1', self.user.username)

        def fail_mock(url, request):
            self.fail('Request should not be fired when using cache.')

        with HTTMock(fail_mock):
            login_url = intershift_plugin._generate_login_url('site1', self.user.username)
        self.assertEquals(login_url, self.test_login_url)

    def test_get_login_url_key(self):
        """ Test _get_login_url_key() """
        self.assertEquals(intershift_plugin._get_login_url_key('site1'), 'INTERSHIFT_SITE1_SSO_URL')

    def test_get_login_url(self):
        """ Test _get_login_url() """

        def key_mock(url, request):
            return self.test_xml

        with HTTMock(key_mock):
            login_url = intershift_plugin._get_login_url('site1', self.user)
        self.assertEquals(login_url, self.test_login_url)

    def test_get_login_urls(self):
        """ Test _get_login_urls() """
        self.request.user = self.user

        def key_mock(url, request):
            return self.test_xml

        with HTTMock(key_mock):
            urls = intershift_plugin.get_login_urls(self.request)
        self.assertEquals(urls, self.test_login_urls)

    def test_integration(self):
        """ Test integration with login_urls() RequestContextProcessor """
        self.request.user = self.user

        def key_mock(url, request):
            return self.test_xml

        with HTTMock(key_mock):
            context = login_urls(self.request)
            self.assertEquals(context, self.test_login_urls)