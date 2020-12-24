# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/kdf/hkdf.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 3463 bytes
from __future__ import absolute_import, division, print_function
import six
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, InvalidKey, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.interfaces import HMACBackend
from cryptography.hazmat.primitives import constant_time, hmac
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction

@utils.register_interface(KeyDerivationFunction)
class HKDF(object):

    def __init__(self, algorithm, length, salt, info, backend):
        if not isinstance(backend, HMACBackend):
            raise UnsupportedAlgorithm('Backend object does not implement HMACBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        else:
            self._algorithm = algorithm
            if salt is None:
                salt = b'\x00' * self._algorithm.digest_size
            else:
                utils._check_bytes('salt', salt)
        self._salt = salt
        self._backend = backend
        self._hkdf_expand = HKDFExpand(self._algorithm, length, info, backend)

    def _extract(self, key_material):
        h = hmac.HMAC((self._salt), (self._algorithm), backend=(self._backend))
        h.update(key_material)
        return h.finalize()

    def derive(self, key_material):
        utils._check_byteslike('key_material', key_material)
        return self._hkdf_expand.derive(self._extract(key_material))

    def verify(self, key_material, expected_key):
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey


@utils.register_interface(KeyDerivationFunction)
class HKDFExpand(object):

    def __init__(self, algorithm, length, info, backend):
        if not isinstance(backend, HMACBackend):
            raise UnsupportedAlgorithm('Backend object does not implement HMACBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        else:
            self._algorithm = algorithm
            self._backend = backend
            max_length = 255 * algorithm.digest_size
            if length > max_length:
                raise ValueError('Can not derive keys larger than {} octets.'.format(max_length))
            self._length = length
            if info is None:
                info = b''
            else:
                utils._check_bytes('info', info)
        self._info = info
        self._used = False

    def _expand(self, key_material):
        output = [
         b'']
        counter = 1
        while self._algorithm.digest_size * (len(output) - 1) < self._length:
            h = hmac.HMAC(key_material, (self._algorithm), backend=(self._backend))
            h.update(output[(-1)])
            h.update(self._info)
            h.update(six.int2byte(counter))
            output.append(h.finalize())
            counter += 1

        return (b'').join(output)[:self._length]

    def derive(self, key_material):
        utils._check_byteslike('key_material', key_material)
        if self._used:
            raise AlreadyFinalized
        self._used = True
        return self._expand(key_material)

    def verify(self, key_material, expected_key):
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey