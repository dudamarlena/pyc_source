# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/SymmetricCryptoKey.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1488 bytes
import bitwarden_simple_cli.enums.EncryptionType as EncryptionType
from base64 import b64encode

class SymmetricCryptoKey:
    key = None
    encKey = None
    macKey = None
    encType = None
    keyB64 = None
    encKeyB64 = None
    macKeyB64 = None
    meta = None

    def __init__(self, key, enc_type=None):
        if not key:
            raise Exception('Must provide ke')
        else:
            if enc_type is None:
                if len(key) == 32:
                    enc_type = EncryptionType.AesCbc256_B64
                else:
                    if len(key) == 64:
                        enc_type = EncryptionType.AesCbc256_HmacSha256_B64
                    else:
                        raise Exception('Unable to determine encType.')
            self.key = key
            self.encType = enc_type
            if enc_type == EncryptionType.AesCbc256_B64 and len(key) == 32:
                self.encKey = key
                self.macKey = None
            else:
                if enc_type == EncryptionType.AesCbc128_HmacSha256_B64 and len(key) == 32:
                    self.encKey = key[0:16]
                    self.macKey = key[16:32]
                else:
                    if enc_type == EncryptionType.AesCbc256_HmacSha256_B64 and len(key) == 64:
                        self.encKey = key[0:32]
                        self.macKey = key[32:64]
                    else:
                        raise Exception('Unsupported encType/key length.')
        if self.key:
            self.keyB64 = b64encode(self.key)
        if self.encKey:
            self.encKeyB64 = b64encode(self.encKey)
        if self.macKey:
            self.macKeyB64 = b64encode(self.macKey)