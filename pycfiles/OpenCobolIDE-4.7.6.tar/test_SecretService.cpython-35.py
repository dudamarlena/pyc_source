# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/tests/backends/test_SecretService.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 976 bytes
import unittest
from ..test_backend import BackendBasicTests
from keyring.backends import SecretService
from .. import util

@unittest.skipUnless(SecretService.Keyring.viable, 'SecretStorage package is needed for SecretServiceKeyring')
class SecretServiceKeyringTestCase(BackendBasicTests, unittest.TestCase):
    __test__ = True

    def init_keyring(self):
        print('Testing SecretServiceKeyring; the following password prompts are for this keyring')
        keyring = SecretService.Keyring()
        keyring.preferred_collection = '/org/freedesktop/secrets/collection/session'
        return keyring


class SecretServiceKeyringUnitTests(unittest.TestCase):

    def test_supported_no_secretstorage(self):
        """
        SecretService Keyring is not viable if secretstorage can't be imported.
        """
        with util.NoNoneDictMutator(SecretService.__dict__, secretstorage=None):
            self.assertFalse(SecretService.Keyring.viable)