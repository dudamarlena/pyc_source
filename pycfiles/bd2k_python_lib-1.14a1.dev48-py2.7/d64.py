# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/d64.py
# Compiled at: 2018-05-03 13:55:55
from __future__ import division
import codecs
from builtins import bytes
from builtins import range
from builtins import object
from past.utils import old_div

class D64(object):

    def __init__(self, special_chars):
        super(D64, self).__init__()
        alphabet = 'PYFGCRLAOEUIDHTNSQJKXBMWVZpyfgcrlaoeuidhtnsqjkxbmwvz1234567890'
        self.alphabet = bytearray(str(('').join(sorted(alphabet + special_chars))).encode('utf-8'))
        self.lookup = bytearray(255)
        for i in range(64):
            code = self.alphabet[i]
            self.lookup[code] = i

    def encode(self, data):
        r"""
        >>> encode = standard.encode
        >>> encode(b'')  # doctest: +ALLOW_UNICODE
        ''
        >>> encode(b'\x00')  # doctest: +ALLOW_UNICODE
        '..'
        >>> encode(b'\x00\x01')  # doctest: +ALLOW_UNICODE
        '..3'
        >>> encode(b'\x00\x01\x02')  # doctest: +ALLOW_UNICODE
        '..31'
        >>> encode(b'\x00\x01\x02\x03\x04\x05\x06\x07')  # doctest: +ALLOW_UNICODE
        '..31.kF40VR'
        """
        data = bytes(data)
        l = len(data)
        s = bytearray(old_div(l * 4 + 2, 3))
        hang = 0
        j = 0
        a = self.alphabet
        for i in range(l):
            v = data[i]
            r = i % 3
            if r == 0:
                s[j] = a[(v >> 2)]
                j += 1
                hang = (v & 3) << 4
            elif r == 1:
                s[j] = a[(hang | v >> 4)]
                j += 1
                hang = (v & 15) << 2
            elif r == 2:
                s[j] = a[(hang | v >> 6)]
                j += 1
                s[j] = a[(v & 63)]
                j += 1
                hang = 0
            elif not False:
                raise AssertionError

        if l % 3:
            s[j] = a[hang]
        return codecs.decode(s)

    def decode(self, e):
        r"""
        >>> import codecs
        >>> decode = standard.decode
        >>> codecs.decode(decode(''), 'unicode-escape') # doctest: +ALLOW_UNICODE
        ''
        >>> codecs.decode(decode('..'), 'unicode-escape') # doctest: +ALLOW_UNICODE
        '\x00'
        >>> codecs.decode(decode('..3'), 'unicode-escape') # doctest: +ALLOW_UNICODE
        '\x00\x01'
        >>> codecs.decode(decode('..31'), 'unicode-escape') # doctest: +ALLOW_UNICODE
        '\x00\x01\x02'
        >>> codecs.decode(decode('..31.kF40VR'), 'unicode-escape') # doctest: +ALLOW_UNICODE
        '\x00\x01\x02\x03\x04\x05\x06\x07'
        """
        n = len(e)
        j = 0
        b = bytearray(old_div(n * 3, 4))
        hang = 0
        l = self.lookup
        for i in range(n):
            v = l[ord(e[i])]
            r = i % 4
            if r == 0:
                hang = v << 2
            elif r == 1:
                b[j] = hang | v >> 4
                j += 1
                hang = v << 4 & 255
            elif r == 2:
                b[j] = hang | v >> 2
                j += 1
                hang = v << 6 & 255
            elif r == 3:
                b[j] = hang | v
                j += 1
            elif not False:
                raise AssertionError

        return bytes(b)


standard = D64('._')