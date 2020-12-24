# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/twofactor/hotp.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 2589 bytes
from __future__ import absolute_import, division, print_function
import struct, six
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.interfaces import HMACBackend
from cryptography.hazmat.primitives import constant_time, hmac
from cryptography.hazmat.primitives.hashes import SHA1, SHA256, SHA512
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.utils import _generate_uri

class HOTP(object):

    def __init__(self, key, length, algorithm, backend, enforce_key_length=True):
        if not isinstance(backend, HMACBackend):
            raise UnsupportedAlgorithm('Backend object does not implement HMACBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        else:
            if len(key) < 16:
                if enforce_key_length is True:
                    raise ValueError('Key length has to be at least 128 bits.')
            else:
                if not isinstance(length, six.integer_types):
                    raise TypeError('Length parameter must be an integer type.')
                if length < 6 or length > 8:
                    raise ValueError('Length of HOTP has to be between 6 to 8.')
            raise isinstance(algorithm, (SHA1, SHA256, SHA512)) or TypeError('Algorithm must be SHA1, SHA256 or SHA512.')
        self._key = key
        self._length = length
        self._algorithm = algorithm
        self._backend = backend

    def generate(self, counter):
        truncated_value = self._dynamic_truncate(counter)
        hotp = truncated_value % 10 ** self._length
        return '{0:0{1}}'.format(hotp, self._length).encode()

    def verify(self, hotp, counter):
        if not constant_time.bytes_eq(self.generate(counter), hotp):
            raise InvalidToken('Supplied HOTP value does not match.')

    def _dynamic_truncate(self, counter):
        ctx = hmac.HMAC(self._key, self._algorithm, self._backend)
        ctx.update(struct.pack('>Q', counter))
        hmac_value = ctx.finalize()
        offset = six.indexbytes(hmac_value, len(hmac_value) - 1) & 15
        p = hmac_value[offset:offset + 4]
        return struct.unpack('>I', p)[0] & 2147483647

    def get_provisioning_uri(self, account_name, counter, issuer):
        return _generate_uri(self, 'hotp', account_name, issuer, [
         (
          'counter', int(counter))])