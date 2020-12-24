# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth/utils/googleotp/googleotp.py
# Compiled at: 2019-04-01 22:50:51
# Size of source mod 2**32: 2283 bytes
from __future__ import print_function, unicode_literals, division, absolute_import
import base64, hashlib, hmac

class OTP(object):

    def __init__(self, s, digits=6, digest=hashlib.sha1):
        """
        @param [String] secret in the form of base32
        @option options digits [Integer] (6)
            Number of integers in the OTP
            Google Authenticate only supports 6 currently
        @option options digest [Callable] (hashlib.sha1)
            Digest used in the HMAC
            Google Authenticate only supports 'sha1' currently
        @returns [OTP] OTP instantiation
        """
        self.digits = digits
        self.digest = digest
        self.secret = s

    def generate_otp(self, input):
        """
        @param [Integer] input the number used seed the HMAC
        Usually either the counter, or the computed integer
        based on the Unix timestamp
        """
        hmac_hash = hmac.new(self.byte_secret(), self.int_to_bytestring(input), self.digest).digest()
        hmac_hash = bytearray(hmac_hash)
        offset = hmac_hash[(-1)] & 15
        code = (hmac_hash[offset] & 127) << 24 | (hmac_hash[(offset + 1)] & 255) << 16 | (hmac_hash[(offset + 2)] & 255) << 8 | hmac_hash[(offset + 3)] & 255
        str_code = str(code % 10 ** self.digits)
        while len(str_code) < self.digits:
            str_code = '0' + str_code

        return str_code

    def byte_secret(self):
        missing_padding = len(self.secret) % 8
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        return base64.b32decode((self.secret), casefold=True)

    @staticmethod
    def int_to_bytestring(i, padding=8):
        """
        Turns an integer to the OATH specified
        bytestring, which is fed to the HMAC
        along with the secret
        """
        result = bytearray()
        while i != 0:
            result.append(i & 255)
            i >>= 8

        return bytes(bytearray(reversed(result)).rjust(padding, b'\x00'))