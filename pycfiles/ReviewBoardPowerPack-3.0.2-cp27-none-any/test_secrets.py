# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/tests/test_secrets.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import with_statement
from django.test import SimpleTestCase
from rbpowerpack.sshdb.secrets import get_sshdb_secret_key

class SecretsTests(SimpleTestCase):
    TEST_SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz123456'
    TEST_BIG_SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz1234567890'

    def test_get_sshdb_secret_key_precedence(self):
        """Testing get_sshdb_secret_key precedence"""
        key1 = self.TEST_SECRET_KEY
        key2 = self.TEST_SECRET_KEY.upper()
        with self.settings(SSHDB_SECRET_KEY=key1, SECRET_KEY=key2):
            self.assertEqual(get_sshdb_secret_key(), key1)

    def test_get_sshdb_secret_key_with_django_secret_key(self):
        """Testing get_sshdb_secret_key with valid SECRET_KEY"""
        with self.settings(SECRET_KEY=self.TEST_SECRET_KEY, SSHDB_SECRET_KEY=None):
            self.assertEqual(get_sshdb_secret_key(), self.TEST_SECRET_KEY)
        return

    def test_get_sshdb_secret_key_with_long_django_secret_key(self):
        """Testing get_sshdb_secret_key with valid but long SECRET_KEY"""
        with self.settings(SECRET_KEY=self.TEST_BIG_SECRET_KEY, SSHDB_SECRET_KEY=None):
            self.assertEqual(get_sshdb_secret_key(), self.TEST_SECRET_KEY)
        return

    def test_get_sshdb_secret_key_with_invalid_django_secret_key(self):
        """Testing get_sshdb_secret_key with invalid SECRET_KEY"""
        with self.settings(SECRET_KEY='small', SSHDB_SECRET_KEY=None):
            self.assertEqual(get_sshdb_secret_key(), None)
        return

    def test_get_sshdb_secret_key_with_sshdb_secret_key(self):
        """Testing get_sshdb_secret_key with valid SSHDB_SECRET_KEY"""
        with self.settings(SSHDB_SECRET_KEY=self.TEST_SECRET_KEY):
            self.assertEqual(get_sshdb_secret_key(), self.TEST_SECRET_KEY)

    def test_get_sshdb_secret_key_with_long_sshdb_secret_key(self):
        """Testing get_sshdb_secret_key with valid but long SSHDB_SECRET_KEY"""
        with self.settings(SSHDB_SECRET_KEY=self.TEST_BIG_SECRET_KEY):
            self.assertEqual(get_sshdb_secret_key(), self.TEST_SECRET_KEY)

    def test_get_sshdb_secret_key_with_invalid_sshdb_secret_key(self):
        """Testing get_sshdb_secret_key with invalid SSHDB_SECRET_KEY"""
        with self.settings(SSHDB_SECRET_KEY='small'):
            self.assertEqual(get_sshdb_secret_key(), None)
        return

    def test_has_valid_sshdb_secret_key_with_valid(self):
        """Testing has_valid_sshdb_secret_key with valid keys"""
        with self.settings(SSHDB_SECRET_KEY=self.TEST_BIG_SECRET_KEY):
            self.assertTrue(get_sshdb_secret_key())

    def test_has_valid_sshdb_secret_key_with_invalid(self):
        """Testing has_valid_sshdb_secret_key with invalid keys"""
        with self.settings(SSHDB_SECRET_KEY='small'):
            self.assertFalse(get_sshdb_secret_key())