# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/twofactor/totp.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 1594 bytes
from __future__ import absolute_import, division, print_function
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.interfaces import HMACBackend
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import HOTP
from cryptography.hazmat.primitives.twofactor.utils import _generate_uri

class TOTP(object):

    def __init__(self, key, length, algorithm, time_step, backend, enforce_key_length=True):
        if not isinstance(backend, HMACBackend):
            raise UnsupportedAlgorithm('Backend object does not implement HMACBackend.', _Reasons.BACKEND_MISSING_INTERFACE)
        self._time_step = time_step
        self._hotp = HOTP(key, length, algorithm, backend, enforce_key_length)

    def generate(self, time):
        counter = int(time / self._time_step)
        return self._hotp.generate(counter)

    def verify(self, totp, time):
        if not constant_time.bytes_eq(self.generate(time), totp):
            raise InvalidToken('Supplied TOTP value does not match.')

    def get_provisioning_uri(self, account_name, issuer):
        return _generate_uri(self._hotp, 'totp', account_name, issuer, [
         (
          'period', int(self._time_step))])