# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_extensions/lib/cryptography.py
# Compiled at: 2017-08-14 04:58:21
# Size of source mod 2**32: 2428 bytes
import base64, hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
    __doc__ = '\n    Adapted solution from: https://stackoverflow.com/a/21928790/1481040\n    '

    def __init__(self):
        self.bs = 32

    def encrypt(self, raw, key, iv=None):
        raw = self._pad(raw)
        if iv is None:
            iv = Random.new().read(AES.block_size)
        hashkey = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(hashkey, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc, key):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        hashkey = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(hashkey, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]