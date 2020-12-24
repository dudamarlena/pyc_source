# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/tests/test_api.py
# Compiled at: 2017-04-21 21:25:05
# Size of source mod 2**32: 607 bytes
from django.test import TestCase
from django.test.utils import override_settings
from google_address.api import GoogleAddressApi

class GoogleAddressApiTestCase(TestCase):

    def test_can_request_without_key(self):
        """ Assert it's possible to make requests without setting a key """
        url = GoogleAddressApi()._get_url()
        self.assertTrue('key=' not in url)

    @override_settings(GOOGLE_ADDRESS={'API_KEY': 'test'})
    def test_can_request_with_key(self):
        """ Assert it's possible to make requests setting a key """
        url = GoogleAddressApi()._get_url()
        self.assertTrue('key=test' in url)