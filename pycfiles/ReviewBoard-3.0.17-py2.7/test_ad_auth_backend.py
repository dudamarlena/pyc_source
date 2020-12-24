# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/tests/test_ad_auth_backend.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for ActiveDirectoryBackend."""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from reviewboard.accounts.backends import ActiveDirectoryBackend
from reviewboard.testing import TestCase

class ActiveDirectoryBackendTests(TestCase):
    """Unit tests for ActiveDirectoryBackend."""

    def test_get_or_create_user_without_ad_user_data_and_with_user(self):
        """Testing ActiveDirectoryBackend.get_or_create_user without
        ad_user_data and with user in database
        """
        backend = ActiveDirectoryBackend()
        user = User.objects.create(username=b'test')
        self.assertEqual(backend.get_or_create_user(b'test', None), user)
        return

    def test_get_or_create_user_without_ad_user_data_and_without_user(self):
        """Testing ActiveDirectoryBackend.get_or_create_user without
        ad_user_data and with user not in database
        """
        backend = ActiveDirectoryBackend()
        self.assertIsNone(backend.get_or_create_user(b'test', None))
        return