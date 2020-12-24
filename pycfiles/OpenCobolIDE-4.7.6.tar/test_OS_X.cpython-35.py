# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/tests/backends/test_OS_X.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 394 bytes
import sys, unittest
from ..test_backend import BackendBasicTests
from keyring.backends import OS_X

def is_osx_keychain_supported():
    return sys.platform in ('mac', 'darwin')


@unittest.skipUnless(is_osx_keychain_supported(), 'Need OS X')
class OSXKeychainTestCase(BackendBasicTests, unittest.TestCase):

    def init_keyring(self):
        return OS_X.Keyring()