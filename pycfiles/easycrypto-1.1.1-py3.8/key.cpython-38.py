# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/easycrypto/key.py
# Compiled at: 2020-01-21 09:12:42
# Size of source mod 2**32: 882 bytes
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class Key:
    ITERATION_COUNT = 10000
    KEY_SIZE = 32

    @classmethod
    def generate(cls, password, password_salt_size):
        salt = os.urandom(password_salt_size)
        return (cls.generate_with_salt(password, salt), salt)

    @classmethod
    def generate_with_salt(cls, password, salt):
        kdf = PBKDF2HMAC(algorithm=(hashes.SHA256()),
          length=(cls.KEY_SIZE),
          salt=salt,
          iterations=(cls.ITERATION_COUNT),
          backend=(default_backend()))
        try:
            pwd_in_bytes = bytes(password, 'utf-8')
        except TypeError:
            pwd_in_bytes = bytes(password)
        else:
            return kdf.derive(pwd_in_bytes)