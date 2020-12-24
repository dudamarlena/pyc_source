# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /data/neo/Proyectos/Python/cryha/test/test_cryha.py
# Compiled at: 2009-05-30 07:20:00
__doc__ = 'Test suite for the Cryha module.'
__author__ = 'Jonás Melián <devel@jonasmelian.com>'
__copyright__ = '(c) 2009 Jonás Melián'
__license__ = 'Apache 2.0'
import os
from nose import tools
from cryha import common
import cryha

class TestHasher:
    schema = common.Schema()
    hasher1 = cryha.Hasher()
    hasher2 = cryha.Hasher(hasher='sha256', salt_size=192)
    hasher = {1: hasher1, 2: hasher2}
    KEY = 'my pass'
    BAD_KEY = 'My pass'
    BAD_HASH = '$5gIhG5rSKdsXjA==$QHy/BrurDcKbVuQI/TMo='
    HASH1 = hasher1.create(KEY)
    HASH2 = hasher2.create(KEY)
    HASH = {1: HASH1, 2: HASH2}

    def test_create(self):
        """Should create a valid hash schema"""
        for i in self.HASH.keys():
            assert self.schema.valid(self.HASH[i], crypter=False)

    def test_bad_schema(self):
        """Should raise HashError"""
        tools.assert_raises(common.HashError, self.schema.valid, self.BAD_HASH, crypter=False)

    def test_compare_ok(self):
        """Hasher should compare successfully to the original key"""
        for i in self.hasher.keys():
            assert self.hasher[i].valid(self.KEY, self.HASH[i])

    def test_compare_no(self):
        """Hasher should compare unsuccessfully to the original key"""
        for i in self.hasher.keys():
            assert not self.hasher[i].valid(self.BAD_KEY, self.HASH[i])


class TestCrypter:
    schema = common.Schema()
    crypter1 = cryha.Crypter(dir_keyfile='test_crypter1')
    crypter2 = cryha.Crypter(cipher='serpent', mode='cbc', key_size=32, dir_keyfile='test_crypter2')
    crypter = {1: crypter1, 2: crypter2}
    KEY = 'myemail@hotmal.com'
    BAD_KEY = 'Myemail@hotmal.com'
    BAD_CRYPT = '$22$BnUEr/9CtJwA=$99L9QagV1oJxH9V'
    CRYPT1 = crypter1.encrypt(KEY)
    CRYPT2 = crypter2.encrypt(KEY)
    CRYPT = {1: CRYPT1, 2: CRYPT2}
    for i in crypter.keys():
        os.remove(crypter[i]._keyfile)
        os.rmdir(crypter[i]._dirname_keyfile)

    def test_create(self):
        """Should create a valid crypt schema"""
        for i in self.CRYPT.keys():
            assert self.schema.valid(self.CRYPT[i])

    def test_bad_schema(self):
        """Should raise CryptError"""
        tools.assert_raises(common.CryptError, self.schema.valid, self.BAD_CRYPT)

    def test_compare_ok(self):
        """Crypter should compare successfully to the original key"""
        for i in self.crypter.keys():
            assert self.crypter[i].decrypt(self.CRYPT[i]) == self.KEY

    def test_compare_no(self):
        """Crypter should compare unsuccessfully to the original key"""
        for i in self.crypter.keys():
            assert not self.crypter[i].decrypt(self.CRYPT[i]) == self.BAD_KEY