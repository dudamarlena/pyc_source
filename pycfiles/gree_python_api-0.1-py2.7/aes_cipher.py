# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/gree-python-api/aes_cipher.py
# Compiled at: 2018-05-14 16:26:59
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    BLOCK_SIZE = 16

    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, msg):
        return self.cipher.encrypt(pad(msg, self.BLOCK_SIZE))

    def decrypt(self, msg):
        return unpad(self.cipher.decrypt(msg), self.BLOCK_SIZE)