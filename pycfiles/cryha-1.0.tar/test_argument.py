# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/neo/Proyectos/Python/cryha/test/test_argument.py
# Compiled at: 2009-05-28 08:59:46
"""Test suite for the Cryha arguments."""
__author__ = 'Jonás Melián <devel@jonasmelian.com>'
__copyright__ = '(c) 2009 Jonás Melián'
__license__ = 'Apache 2.0'
import os
from nose import tools
import cryha

class TestHasher:
    """Check arguments passed to Hasher."""

    def test_hasher(self):
        for hasher in [None, 'non_exist']:
            yield (
             self.check_hasher, hasher, None)

        hasher = 'tiger'
        for salt_size in [None, '10', '10s']:
            yield (
             self.check_hasher, hasher, salt_size)

        return

    def check_hasher(self, hasher, salt_size):
        tools.assert_raises(ValueError, cryha.Hasher, hasher=hasher, salt_size=salt_size)


class TestCrypter:
    """Check arguments passed to Crypter."""

    def test_crypter(self):
        for cipher in [None, 'non_exist']:
            yield (
             self.check_crypter, cipher, None, None, None)

        cipher = 'serpent'
        for mode in [None, 'non_exist']:
            yield (
             self.check_crypter, cipher, mode, None, None)

        mode = 'cbc'
        for key_size in [None, '10s', 10]:
            yield (
             self.check_crypter, cipher, mode, key_size, None)

        key_size = 16
        yield (
         self.check_crypter, cipher, mode, key_size, None, None)
        file_path = os.path.abspath(os.path.dirname(__file__))
        yield (self.check_crypter, cipher, mode, key_size, file_path, __file__)
        return

    def check_crypter(self, cipher, mode, key_size, root_keyfile, dir_keyfile='test-0'):
        tools.assert_raises(ValueError, cryha.Crypter, cipher=cipher, mode=mode, key_size=key_size, root_keyfile=root_keyfile, dir_keyfile=dir_keyfile)