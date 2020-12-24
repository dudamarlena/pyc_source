# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drbob/Development/hap-intra/env/src/django-url-sso/url_sso/tests/context_processor.py
# Compiled at: 2014-02-06 11:37:55
""" Common tests seperate from plugins. """
from django.test import TestCase
from url_sso.context_processors import login_urls
from .mock_plugins import mock_plugin_one
from .utils import RequestTestMixin

class ContextProcessorTests(RequestTestMixin, TestCase):
    """ Test for context processor """

    def test_no_plugins(self):
        """ Test login URL's when no plugins are configured """
        with self.settings(URL_SSO_PLUGINS=[]):
            self.assertEquals(login_urls(self.request), {})

    def test_mock_plugin(self):
        """ Test with a mock plugin """
        sso_plugins = [
         'url_sso.tests.mock_plugins.mock_plugin_one']
        with self.settings(URL_SSO_PLUGINS=sso_plugins):
            self.assertEquals(login_urls(self.request), mock_plugin_one.bogus_dict)

    def test_exception(self):
        """ Test with a mock plugin raising a RequestKeyException """
        sso_plugins = [
         'url_sso.tests.mock_plugins.mock_plugin_exception']
        with self.settings(URL_SSO_PLUGINS=sso_plugins):
            self.assertEquals(login_urls(self.request), {})

    def test_two_plugins(self):
        """ Test with two bogus plugins """
        sso_plugins = [
         'url_sso.tests.mock_plugins.mock_plugin_one',
         'url_sso.tests.mock_plugins.mock_plugin_two']
        with self.settings(URL_SSO_PLUGINS=sso_plugins):
            self.assertEquals(login_urls(self.request), {'MY_URL': 'https://www.bogus.com/some_token', 
               'OTHER_URL': 'https://www.bogus.com/other_token'})