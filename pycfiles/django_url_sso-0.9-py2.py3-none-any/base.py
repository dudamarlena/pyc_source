# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drbob/Development/hap-intra/env/src/django-url-sso/url_sso/tests/plugins/base.py
# Compiled at: 2014-02-06 10:16:17
from httmock import HTTMock
from django.test import TestCase
from django.test.utils import override_settings
from ..mock_plugins import mock_plugin_one
from url_sso.exceptions import RequestKeyException

class BaseTests(TestCase):
    """ Test functionality from SSOPluginBase """

    @override_settings(URL_SSO_ONE={'TEST': True})
    def test_get_settings(self):
        """ Test _get_settings() """
        settings = mock_plugin_one.get_settings()
        self.assertEquals(settings, {'TEST': True})

    def test_get_url(self):
        """ Test get_url() """

        def success_mock(url, request):
            return 'success'

        with HTTMock(success_mock):
            r = mock_plugin_one.get_url('https://www.bogus.com/')
            self.assertEquals(r.status_code, 200)
            self.assertEquals(r.content, 'success')

    def test_get_url_exception(self):
        """ Test get_url() exception """
        self.assertRaises(RequestKeyException, lambda : mock_plugin_one.get_url('https://weirddomainnamethatdoesnotexist3423423432.com/'))