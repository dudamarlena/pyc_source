# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/hmac.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 2196 bytes
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.interfaces import HMACBackend
from cryptography.hazmat.primitives import hashes

@utils.register_interface(hashes.HashContext)
class HMAC(object):

    def __init__(self, key, algorithm, backend, ctx=None):
        if not isinstance(backend, HMACBackend):
            raise UnsupportedAlgorithm('Backend object does not implement HMACBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        else:
            if not isinstance(algorithm, hashes.HashAlgorithm):
                raise TypeError('Expected instance of hashes.HashAlgorithm.')
            self._algorithm = algorithm
            self._backend = backend
            self._key = key
            if ctx is None:
                self._ctx = self._backend.create_hmac_ctx(key, self.algorithm)
            else:
                self._ctx = ctx

    algorithm = utils.read_only_property('_algorithm')

    def update(self, data):
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        utils._check_byteslike('data', data)
        self._ctx.update(data)

    def copy(self):
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        return HMAC((self._key),
          (self.algorithm),
          backend=(self._backend),
          ctx=(self._ctx.copy()))

    def finalize(self):
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        digest = self._ctx.finalize()
        self._ctx = None
        return digest

    def verify(self, signature):
        utils._check_bytes('signature', signature)
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        ctx, self._ctx = self._ctx, None
        ctx.verify(signature)