# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\crypto\pure\AES\util.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 2172 bytes


def to_bufferable(binary):
    return binary


def _get_byte(c):
    return ord(c)


try:
    xrange
except:

    def to_bufferable(binary):
        if isinstance(binary, bytes):
            return binary
        return bytes((ord(b) for b in binary))


    def _get_byte(c):
        return c


def append_PKCS7_padding(data):
    pad = 16 - len(data) % 16
    return data + to_bufferable(chr(pad) * pad)


def strip_PKCS7_padding(data):
    if len(data) % 16 != 0:
        raise ValueError('invalid length')
    pad = _get_byte(data[(-1)])
    if pad > 16:
        raise ValueError('invalid padding byte')
    return data[:-pad]