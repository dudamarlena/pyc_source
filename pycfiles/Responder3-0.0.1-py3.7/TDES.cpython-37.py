# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\crypto\TDES.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 3228 bytes
"""
The idea here is to offer compatibility with 3rd party libraries by extending wrappers for ech encryption mode
This is needed because the pure python implementation for encryption and hashing algorithms are quite slow

currently it's not the perfect wrapper, needs to be extended
"""
from responder3.crypto.BASE import symmetricBASE, cipherMODE, padMode
import responder3.crypto.pure.DES.DES as _pyDES
try:
    import Crypto.Cipher as _pyCryptoDES3
except:
    pass

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
except:
    pass

class pureTDES(symmetricBASE):

    def __init__(self, key, mode=cipherMODE.ECB, IV=None, pad=None, padMode=None):
        symmetricBASE.__init__(self)
        if not isinstance(key, bytes):
            raise Exception('Key needs to be bytes!')
        self.mode = mode
        self.IV = IV
        self.pad = pad
        self.padMode = padMode

    def setup_cipher(self):
        if self.mode == cipherMODE.ECB:
            mode = _pyDes.ECB
            self._cipher = _pyDES.triple_des(self.key, mode)
        else:
            if self.mode == cipherMODE.CBC:
                mode = _pyDES.CBC
                if padMode is None:
                    self._cipher = _pyDES.triple_des(self.key, mode, self.IV, self.pad, self.padmode)
                else:
                    self._cipher = _pyDES.triple_des(self.key, mode, self.IV)
            else:
                raise Exception('Unknown cipher mode!')

    def encrypt(self, data):
        return self._cipher.encrypt(data)

    def decrypt(self, data):
        return self._cipher.decrypt(data)


class pyCryptoTDES(symmetricBASE):

    def __init__(self, key, mode=cipherMODE.ECB, IV=None, pad=None, padMode=None):
        self.key = key
        self.mode = mode
        self.IV = IV
        self.pad = pad
        self.padMode = padMode
        symmetricBASE.__init__(self)

    def setup_cipher(self):
        if self.mode == cipherMODE.ECB:
            self._cipher = _pyCryptoDES3.new(self.key, _pyCryptoDES3.MODE_ECB)
        else:
            if self.mode == cipherMODE.CBC:
                self._cipher = _pyCryptoDES3.new(self.key, _pyCryptoDES3.MODE_CBC, self.IV)
            else:
                raise Exception('Unknown cipher mode!')

    def encrypt(self, data):
        return self._cipher.encrypt(data)

    def decrypt(self, data):
        return self._cipher.decrypt(data)


class cryptographyTDES(symmetricBASE):

    def __init__(self, key, mode=cipherMODE.ECB, IV=None, pad=None, padMode=None):
        if not isinstance(key, bytes):
            raise Exception('Key needs to be bytes!')
        else:
            self.IV = IV
            if mode == cipherMode.ECB:
                self.IV = modes.ECB()
            else:
                if mode == cipherMODE.CBC:
                    self.IV = modes.CBC(IV)
                else:
                    raise Exception('Unknown cipher mode!')
        self.key = key
        self.encryptor = None
        self.decryptor = None
        symmetricBASE.__init__(self)

    def setup_cipher(self):
        algorithm = algorithms.TripleDES(self.key)
        self._cipher = Cipher(algorithm, mode=(self.IV), backend=(default_backend()))
        self.encryptor = self._cipher.encryptor()
        self.decryptor = self._cipher.decryptor()

    def encrypt(self, data):
        return self.encryptor.update(data)

    def decrypt(self, data):
        return self.decryptor.update(data)