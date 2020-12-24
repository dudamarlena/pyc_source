# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/crypto/ecc.py
# Compiled at: 2016-07-10 16:06:16
import six, hashlib, ecdsa
CURVE = ecdsa.SECP256k1

class SigningKey(ecdsa.SigningKey, object):

    def get_pubkey(self):
        return '\x04' + self.get_verifying_key().to_string()

    def sign(self, msg):
        return super(SigningKey, self).sign(msg, sigencode=ecdsa.util.sigencode_der, hashfunc=hashlib.sha256)


class VerifyingKey(ecdsa.VerifyingKey, object):

    def verify(self, signature, data):
        return super(VerifyingKey, self).verify(signature, data, hashfunc=hashlib.sha256, sigdecode=ecdsa.util.sigdecode_der)


def private(seed, salt, kdf=None, curve=CURVE):
    assert callable(kdf)
    if six.PY3 and isinstance(seed, six.string_types):
        seed = seed.encode()
    if isinstance(salt, (list, tuple)):
        salt = ('|').join(salt)
        if six.PY3:
            salt = salt.encode()
    return SigningKey.from_string(kdf(seed, salt), curve=curve)


def public(pub, curve=CURVE):
    assert pub[0] == '\x04'
    return VerifyingKey.from_string(pub[1:], curve=curve)