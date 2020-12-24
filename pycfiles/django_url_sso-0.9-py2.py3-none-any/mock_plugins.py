# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drbob/Development/hap-intra/env/src/django-url-sso/url_sso/tests/mock_plugins.py
# Compiled at: 2014-02-06 11:37:18
""" Mock plugins used for testing. """
from url_sso.exceptions import RequestKeyException
from url_sso.plugins.base import SSOPluginBase

class MockPluginOne(SSOPluginBase):
    settings_name = 'ONE'
    bogus_dict = {'MY_URL': 'https://www.bogus.com/some_token'}

    def get_login_urls(self, request):
        return self.bogus_dict


class MockPluginException(SSOPluginBase):
    settings_name = 'EXCEPTION'

    def get_login_urls(self, request):
        raise RequestKeyException('bananas')


class MockPluginTwo(SSOPluginBase):
    settings_name = 'TWO'
    bogus_dict = {'OTHER_URL': 'https://www.bogus.com/other_token'}

    def get_login_urls(self, request):
        return self.bogus_dict


mock_plugin_one = MockPluginOne()
mock_plugin_exception = MockPluginException()
mock_plugin_two = MockPluginTwo()