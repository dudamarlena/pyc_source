# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpfwd/trunking/crypto.py
# Compiled at: 2018-12-30 12:01:29
from Cryptodome import Random
from Cryptodome.Cipher import AES
from pyasn1.compat.octets import int2oct, oct2int, str2octs

class AESCipher(object):
    __module__ = __name__

    @staticmethod
    def pad(s, BS=16):
        return s + (BS - len(s) % BS) * int2oct(BS - len(s) % BS)

    @staticmethod
    def unpad(s):
        return s[0:-oct2int(s[(-1)])]

    def encrypt(self, key, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(str2octs(key), AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, key, enc):
        iv = enc[:16]
        cipher = AES.new(str2octs(key), AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))


encrypt = AESCipher().encrypt
decrypt = AESCipher().decrypt