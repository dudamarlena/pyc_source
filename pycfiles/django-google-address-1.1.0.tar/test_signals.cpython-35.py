# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/tests/test_signals.py
# Compiled at: 2017-05-03 17:34:38
# Size of source mod 2**32: 710 bytes
from unittest import mock
from django.test import TestCase
from django.test.utils import override_settings
from google_address.signals import address_post_save
from google_address.models import Address

class PostSaveSignalTestCase(TestCase):

    def setUp(self):
        self.instance = Address(raw='Chicago')
        self.instance.save()

    @mock.patch('google_address.update.update_address', return_value=True)
    @override_settings(GOOGLE_ADDRESS={'API_LANGUAGE': 'en_US', 'ASYNC_CALLS': True})
    def test_async_settings(self, mocked_update_address):
        """Assert configuring ASYNC_CALLS setting makes the post_save signal spawn a thread"""
        thread = address_post_save(Address, self.instance)
        thread.join()