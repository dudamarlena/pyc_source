# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/darko/dev/ba-pip/bitcoinaverage/clients/_base_client.py
# Compiled at: 2018-08-30 04:45:48
# Size of source mod 2**32: 1257 bytes
import hmac, time
from hashlib import sha256
from itsdangerous import Signer, SigningAlgorithm, want_bytes

class HexSigningAlgorithm(SigningAlgorithm):

    def get_signature(self, key, value):
        mac = hmac.new(key, msg=value, digestmod=sha256)
        return want_bytes(mac.hexdigest())


class ApiKeySigner(Signer):

    def __init__(self, secret_key):
        super(ApiKeySigner, self).__init__(secret_key, digest_method=sha256, key_derivation='none', algorithm=(HexSigningAlgorithm()))

    def sign(self, value):
        if type(value) is str:
            value = value.encode()
        return super(ApiKeySigner, self).sign(value)

    def get_signature(self, value):
        """Returns the signature for the given value"""
        value = want_bytes(value)
        key = self.derive_key()
        sig = self.algorithm.get_signature(key, value)
        return want_bytes(sig)


class _BaseClient:

    def __init__(self, secret_key, public_key):
        self.secret_key = secret_key
        self.public_key = public_key
        self.signer = ApiKeySigner(secret_key)

    @property
    def signature_header(self):
        return self.signer.sign('{}.{}'.format(int(time.time()), self.public_key))