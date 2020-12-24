# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/wlogger/utils/cryptex.py
# Compiled at: 2015-12-22 05:53:45
"""Crypto module used by ping-me"""
from Crypto.Cipher import AES
import base64, random
mode = AES.MODE_CBC

def encryptor(key, message):
    """Cipher a message using a key"""
    IV = ('').join(chr(random.randint(0, 255)) for i in range(16))
    encrypto = AES.new(key, mode, IV=IV)
    crypt_message = encrypto.encrypt(message)
    cipher = crypt_message + IV
    return base64.b64encode(cipher)


def decryptor(key, cipher):
    """Decipher a crypted message using a key"""
    cipher = base64.b64decode(cipher)
    IV = cipher[-16:]
    decrypt_message = cipher[:-16]
    decrpyto = AES.new(key, mode, IV=IV)
    message = decrpyto.decrypt(decrypt_message)
    return message