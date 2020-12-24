# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\crypto\RC4.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2002 bytes
"""
The idea here is to offer compatibility with 3rd party libraries by extending wrappers for ech encryption mode
This is needed because the pure python implementation for encryption and hashing algorithms are quite slow

currently it's not the perfect wrapper, needs to be extended
"""
from responder3.crypto.BASE import symmetricBASE, cipherMODE
import responder3.crypto.pure.RC4.RC4 as _pureRC4
try:
    import Crypto.Cipher as _pyCryptoRC4
except Exception as e:
    try:
        print(e)
    finally:
        e = None
        del e

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except:
    pass

class pureRC4(symmetricBASE):

    def __init__(self, key):
        if not isinstance(key, bytes):
            raise Exception('Key needs to be bytes!')
        self.key = key
        symmetricBASE.__init__(self)

    def setup_cipher(self):
        self._cipher = _pureRC4(self.key)

    def encrypt(self, data):
        return self._cipher.encrypt(data)

    def decrypt(self, data):
        return self._cipher.decrypt(data)


class pyCryptoRC4(symmetricBASE):

    def __init__(self, key):
        self.key = key
        symmetricBASE.__init__(self)

    def setup_cipher(self):
        self._cipher = _pyCryptoRC4.new(self.key)

    def encrypt(self, data):
        return self._cipher.encrypt(data)

    def decrypt(self, data):
        return self._cipher.decrypt(data)


class cryptographyRC4(symmetricBASE):

    def __init__(self, key):
        if not isinstance(key, bytes):
            raise Exception('Key needs to be bytes!')
        self.key = key
        self.encryptor = None
        self.decryptor = None
        symmetricBASE.__init__(self)

    def setup_cipher(self):
        algorithm = algorithms.ARC4(self.key)
        self._cipher = Cipher(algorithm, mode=None, backend=(default_backend()))
        self.encryptor = self._cipher.encryptor()
        self.decryptor = self._cipher.decryptor()

    def encrypt(self, data):
        return self.encryptor.update(data)

    def decrypt(self, data):
        return self.decryptor.update(data)