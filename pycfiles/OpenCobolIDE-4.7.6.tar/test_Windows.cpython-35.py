# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/tests/backends/test_Windows.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 652 bytes
from __future__ import print_function
import sys, unittest, keyring.backends.Windows
from ..test_backend import BackendBasicTests

@unittest.skipUnless(keyring.backends.Windows.WinVaultKeyring.viable, 'Needs Windows')
class WinVaultKeyringTestCase(BackendBasicTests, unittest.TestCase):

    def tearDown(self):
        for cred in self.credentials_created:
            try:
                self.keyring.delete_password(*cred)
            except Exception as e:
                print(e, file=sys.stderr)

    def init_keyring(self):
        return keyring.backends.Windows.WinVaultKeyring()