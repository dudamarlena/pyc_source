# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/cmac.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 2075 bytes
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.interfaces import CMACBackend
from cryptography.hazmat.primitives import ciphers

class CMAC(object):

    def __init__(self, algorithm, backend, ctx=None):
        if not isinstance(backend, CMACBackend):
            raise UnsupportedAlgorithm('Backend object does not implement CMACBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        else:
            if not isinstance(algorithm, ciphers.BlockCipherAlgorithm):
                raise TypeError('Expected instance of BlockCipherAlgorithm.')
            self._algorithm = algorithm
            self._backend = backend
            if ctx is None:
                self._ctx = self._backend.create_cmac_ctx(self._algorithm)
            else:
                self._ctx = ctx

    def update(self, data):
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        utils._check_bytes('data', data)
        self._ctx.update(data)

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

    def copy(self):
        if self._ctx is None:
            raise AlreadyFinalized('Context was already finalized.')
        return CMAC((self._algorithm),
          backend=(self._backend),
          ctx=(self._ctx.copy()))