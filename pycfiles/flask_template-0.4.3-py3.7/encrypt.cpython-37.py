# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/simple/proj/utils/encrypt.py
# Compiled at: 2020-03-11 03:42:34
# Size of source mod 2**32: 718 bytes
import base64
from Crypto.Cipher import AES
BLOCK_SIZE = 16

def pkcs5_pad(s):
    n = BLOCK_SIZE - len(s) % BLOCK_SIZE
    return s + n * chr(n)


def pkcs5_unpad(s):
    return s[0:-ord(s[(-1)])]


class AESCipher(object):

    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        cipher = AES.new(self.key)
        encrypted = cipher.encrypt(pkcs5_pad(data))
        return base64.b64encode(encrypted).decode()

    def decrypt(self, data):
        cipher = AES.new(self.key)
        decrypted = cipher.decrypt(base64.b64decode(data)).decode()
        return pkcs5_unpad(decrypted)


aes = AESCipher(b'\x96\xf7h\xe3\xd4\xedH\x1c3\xe7\xd6b\x85\x96\xf3\xf2')