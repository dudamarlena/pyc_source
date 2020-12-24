# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\crypto\DES.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2791 bytes
"""
The idea here is to offer compatibility with 3rd party libraries by extending wrappers for ech encryption mode
This is needed because the pure python implementation for encryption and hashing algorithms are quite slow

currently it's not the perfect wrapper, needs to be extended
"""
from responder3.crypto.BASE import symmetricBASE, cipherMODE
import responder3.crypto.pure.DES.DES as _pyDES
try:
    import Crypto.Cipher as _pyCryptoDES
except:
    pass

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except:
    pass

def expand_DES_key(key):
    key = key[:7]
    key += b'\x00' * (7 - len(key))
    s = ((key[0] >> 1 & 127) << 1).to_bytes(1, byteorder='big')
    s += (((key[0] & 1) << 6 | key[1] >> 2 & 63) << 1).to_bytes(1, byteorder='big')
    s += (((key[1] & 3) << 5 | key[2] >> 3 & 31) << 1).to_bytes(1, byteorder='big')
    s += (((key[2] & 7) << 4 | key[3] >> 4 & 15) << 1).to_bytes(1, byteorder='big')
    s += (((key[3] & 15) << 3 | key[4] >> 5 & 7) << 1).to_bytes(1, byteorder='big')
    s += (((key[4] & 31) << 2 | key[5] >> 6 & 3) << 1).to_bytes(1, byteorder='big')
    s += (((key[5] & 63) << 1 | key[6] >> 7 & 1) << 1).to_bytes(1, byteorder='big')
    s += ((key[6] & 127) << 1).to_bytes(1, byteorder='big')
    return s


class pureDES(symmetricBASE):

    def __init__(self, key, mode=cipherMODE.ECB, IV=None):
        self.key = key
        if len(key) == 7:
            self.key = expand_DES_key(key)
        self.mode = mode
        self.IV = IV
        symmetricBASE.__init__(self)

    def setup_cipher(self):
        if self.mode == cipherMODE.ECB:
            mode = _pyDES.ECB
        else:
            if self.mode == cipherMODE.CBC:
                mode = _pyDES.CBC
            else:
                raise Exception('Unknown cipher mode!')
        self._cipher = _pyDES.des(self.key, mode, self.IV)

    def encrypt(self, data):
        return self._cipher.encrypt(data)

    def decrypt(self, data):
        return self._cipher.decrypt(data)


class pyCryptoDES(symmetricBASE):

    def __init__(self, key, mode=cipherMODE.ECB, IV=None):
        self.key = key
        if len(key) == 7:
            self.key = _pyCryptoDES__expand_DES_key(key)
        self.mode = mode
        self.IV = IV
        symmetricBASE.__init__(self)

    def setup_cipher(self):
        if self.mode == cipherMODE.ECB:
            self._cipher = _pyCryptoDES.new(self.key)
        else:
            if self.mode == cipherMODE.CBC:
                self._cipher = _pyCryptoDES.new(self.key, _pyCryptoDES.MODE_CBC, self.IV)
            else:
                raise Exception('Unknown cipher mode!')

    def encrypt(self, data):
        return self._cipher.encrypt(data)

    def decrypt(self, data):
        return self._cipher.decrypt(data)