# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/tests/backends/test_kwallet.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 2956 bytes
import unittest
from keyring.backends import kwallet
from ..test_backend import BackendBasicTests

@unittest.skipUnless(kwallet.DBusKeyring.viable, 'KWallet5 unavailable')
class DBusKWalletTestCase(BackendBasicTests, unittest.TestCase):
    DIFFICULT_CHARS = BackendBasicTests.DIFFICULT_CHARS.replace('@', '')

    def init_keyring(self):
        return kwallet.DBusKeyring()

    def tearDown(self):
        for item in self.credentials_created:
            try:
                self.keyring.delete_password(*item)
            except:
                pass

    def set_password(self, service, username, password, old_format=False):
        self.credentials_created.add((service, username))
        if old_format:
            username = username + '@' + service
            service = 'Python'
        super(DBusKWalletTestCase, self).set_password(service, username, password)

    def check_set_get(self, service, username, password):
        keyring = self.keyring
        self.assertEqual(keyring.get_password(service, username), None)
        self.set_password(service, username, password, True)
        self.keyring = keyring = self.init_keyring()
        ret_password = keyring.get_password(service, username)
        self.assertEqual(ret_password, password, "Incorrect password for username: '%s' on service: '%s'. '%s' != '%s'" % (
         service, username, ret_password, password))
        self.set_password(service, username, '', True)
        self.keyring = keyring = self.init_keyring()
        ret_password = keyring.get_password(service, username)
        self.assertEqual(ret_password, '', "Incorrect password for username: '%s' on service: '%s'. '%s' != '%s'" % (
         service, username, ret_password, ''))
        ret_password = keyring.get_password('Python', username + '@' + service)
        self.assertEqual(ret_password, None, "Not 'None' password returned for username: '%s' on service: '%s'. '%s' != '%s'. Passwords from old folder should be deleted during migration." % (
         service, username, ret_password, None))


@unittest.skipUnless(kwallet.DBusKeyringKWallet4.viable, 'KWallet4 unavailable')
class DBusKWallet4TestCase(DBusKWalletTestCase):

    def init_keyring(self):
        return kwallet.DBusKeyringKWallet4()