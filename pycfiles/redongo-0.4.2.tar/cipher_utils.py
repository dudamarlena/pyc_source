# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgalan/projects/redongo/redongo/cipher_utils.py
# Compiled at: 2016-08-11 11:38:11
import base64
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher:

    def __init__(self, key):
        self.key = key
        self.BS = 16
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        if not raw:
            return 'None'
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        if enc == 'None':
            return None
        else:
            enc = base64.b64decode(enc)
            iv = enc[:16]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self.unpad(cipher.decrypt(enc[16:]))