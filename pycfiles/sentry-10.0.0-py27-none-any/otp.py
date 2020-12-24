# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/utils/otp.py
# Compiled at: 2019-09-04 11:06:02
from __future__ import absolute_import
import six, time, hmac, base64, qrcode, hashlib
from datetime import datetime
from six.moves.urllib.parse import quote
from sentry.utils.dates import to_timestamp
from django.utils.crypto import constant_time_compare, get_random_string

def generate_secret_key(length=32):
    return get_random_string(length, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')


def _pack_int(i):
    result = bytearray()
    while i != 0:
        result.append(i & 255)
        i >>= 8

    return six.binary_type(bytearray(reversed(result)).rjust(8, '\x00'))


def _get_ts(ts):
    if ts is None:
        return int(time.time())
    else:
        if isinstance(ts, datetime):
            return int(to_timestamp(ts))
        return int(ts)


class TOTP(object):

    def __init__(self, secret=None, digits=6, interval=30, default_window=2):
        if secret is None:
            secret = generate_secret_key()
        if len(secret) % 8 != 0:
            raise RuntimeError('Secret length needs to be a multiple of 8')
        self.secret = secret
        self.digits = digits
        self.interval = interval
        self.default_window = default_window
        return

    def generate_otp(self, ts=None, offset=0, counter=None):
        if counter is None:
            ts = _get_ts(ts)
            counter = int(ts) // self.interval + offset
        h = bytearray(hmac.HMAC(base64.b32decode(self.secret.encode('ascii'), casefold=True), _pack_int(counter), hashlib.sha1).digest())
        offset = h[(-1)] & 15
        code = (h[offset] & 127) << 24 | (h[(offset + 1)] & 255) << 16 | (h[(offset + 2)] & 255) << 8 | h[(offset + 3)] & 255
        str_code = six.text_type(code % 10 ** self.digits)
        return '0' * (self.digits - len(str_code)) + str_code

    def verify(self, otp, ts=None, window=None, return_counter=False, check_counter_func=None):
        ts = _get_ts(ts)
        if window is None:
            window = self.default_window
        for i in range(-window, window + 1):
            counter = int(ts) // self.interval + i
            if constant_time_compare(otp, self.generate_otp(counter=counter)):
                if check_counter_func is not None and not check_counter_func(counter):
                    continue
                if return_counter:
                    return counter
                return True

        if return_counter:
            return
        else:
            return False

    def get_provision_url(self, user, issuer=None):
        if issuer is None:
            issuer = 'Sentry'
        rv = 'otpauth://totp/%s?issuer=%s&secret=%s' % (
         quote(user.encode('utf-8')),
         quote(issuer.encode('utf-8')),
         self.secret)
        if self.digits != 6:
            rv += '&digits=%d' % self.digits
        if self.interval != 30:
            rv += '&period=%d' % self.interval
        return rv

    def get_provision_qrcode(self, user, issuer=None):
        qr = qrcode.QRCode(border=0)
        qr.add_data(self.get_provision_url(user, issuer=issuer))
        return [ [ int(c) for c in row ] for row in qr.get_matrix() ]