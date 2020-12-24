# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/kdf/kbkdf.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 4905 bytes
from __future__ import absolute_import, division, print_function
from enum import Enum
from six.moves import range
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, InvalidKey, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.interfaces import HMACBackend
from cryptography.hazmat.primitives import constant_time, hashes, hmac
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction

class Mode(Enum):
    CounterMode = 'ctr'


class CounterLocation(Enum):
    BeforeFixed = 'before_fixed'
    AfterFixed = 'after_fixed'


@utils.register_interface(KeyDerivationFunction)
class KBKDFHMAC(object):

    def __init__(self, algorithm, mode, length, rlen, llen, location, label, context, fixed, backend):
        if not isinstance(backend, HMACBackend):
            raise UnsupportedAlgorithm('Backend object does not implement HMACBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        else:
            if not isinstance(algorithm, hashes.HashAlgorithm):
                raise UnsupportedAlgorithm('Algorithm supplied is not a supported hash algorithm.', _Reasons.UNSUPPORTED_HASH)
            else:
                if not backend.hmac_supported(algorithm):
                    raise UnsupportedAlgorithm('Algorithm supplied is not a supported hmac algorithm.', _Reasons.UNSUPPORTED_HASH)
                elif not isinstance(mode, Mode):
                    raise TypeError('mode must be of type Mode')
                else:
                    if not isinstance(location, CounterLocation):
                        raise TypeError('location must be of type CounterLocation')
                    elif label or context:
                        if fixed:
                            raise ValueError('When supplying fixed data, label and context are ignored.')
                    else:
                        if rlen is None or not self._valid_byte_length(rlen):
                            raise ValueError('rlen must be between 1 and 4')
                        if llen is None:
                            if fixed is None:
                                raise ValueError('Please specify an llen')
                    if llen is not None:
                        if not isinstance(llen, int):
                            raise TypeError('llen must be an integer')
                if label is None:
                    label = b''
            if context is None:
                context = b''
        utils._check_bytes('label', label)
        utils._check_bytes('context', context)
        self._algorithm = algorithm
        self._mode = mode
        self._length = length
        self._rlen = rlen
        self._llen = llen
        self._location = location
        self._label = label
        self._context = context
        self._backend = backend
        self._used = False
        self._fixed_data = fixed

    def _valid_byte_length(self, value):
        if not isinstance(value, int):
            raise TypeError('value must be of type int')
        value_bin = utils.int_to_bytes(1, value)
        if not 1 <= len(value_bin) <= 4:
            return False
        else:
            return True

    def derive(self, key_material):
        if self._used:
            raise AlreadyFinalized
        utils._check_byteslike('key_material', key_material)
        self._used = True
        rounds = -(-self._length // self._algorithm.digest_size)
        output = [
         b'']
        r_bin = utils.int_to_bytes(1, self._rlen)
        if rounds > pow(2, len(r_bin) * 8) - 1:
            raise ValueError('There are too many iterations.')
        for i in range(1, rounds + 1):
            h = hmac.HMAC(key_material, (self._algorithm), backend=(self._backend))
            counter = utils.int_to_bytes(i, self._rlen)
            if self._location == CounterLocation.BeforeFixed:
                h.update(counter)
            h.update(self._generate_fixed_input())
            if self._location == CounterLocation.AfterFixed:
                h.update(counter)
            output.append(h.finalize())

        return (b'').join(output)[:self._length]

    def _generate_fixed_input(self):
        if self._fixed_data:
            if isinstance(self._fixed_data, bytes):
                return self._fixed_data
        l_val = utils.int_to_bytes(self._length * 8, self._llen)
        return (b'').join([self._label, b'\x00', self._context, l_val])

    def verify(self, key_material, expected_key):
        if not constant_time.bytes_eq(self.derive(key_material), expected_key):
            raise InvalidKey