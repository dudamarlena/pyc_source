# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/d32.py
# Compiled at: 2018-05-03 13:55:55
from __future__ import division
import codecs, sys
from builtins import range
from builtins import object
from past.utils import old_div

class D32(object):
    """
    Base32 encoding and decoding without padding, and using an arbitrary alphabet.
    """

    def __init__(self, alphabet):
        super(D32, self).__init__()
        self.alphabet = bytearray(alphabet.encode('utf-8'))
        self.lookup = bytearray(255)
        for i in range(32):
            self.lookup[self.alphabet[i]] = i

    def encode(self, d):
        r"""
        >>> encode = standard.encode
        >>> encode(b'')  # doctest: +ALLOW_UNICODE
        ''
        >>> encode(b'\0')  # doctest: +ALLOW_UNICODE
        '22'
        >>> encode(b'\xff')  # doctest: +ALLOW_UNICODE
        'zw'
        >>> encode(b'\0\1\2\3\4')  # doctest: +ALLOW_UNICODE
        '222k62s6'
        >>> encode(b'\0\1\2\3\4\5')  # doctest: +ALLOW_UNICODE
        '222k62s62o'
        """
        m = len(d)
        n = old_div(m * 8 + 4, 5)
        padding = 8 - n % 8
        e = bytearray(n + padding)
        i, j = (0, 0)
        a = self.alphabet
        while i < m:
            if m - i < 5:
                g = bytearray(d[i:] + '\x00' * (5 - (m - i)))
            else:
                g = bytearray(d[i:i + 5])
            e[j + 0] = a[(g[0] >> 3)]
            e[j + 1] = a[(g[0] << 2 & 31 | g[1] >> 6)]
            e[j + 2] = a[(g[1] >> 1 & 31)]
            e[j + 3] = a[(g[1] << 4 & 31 | g[2] >> 4)]
            e[j + 4] = a[(g[2] << 1 & 31 | g[3] >> 7)]
            e[j + 5] = a[(g[3] >> 2 & 31)]
            e[j + 6] = a[(g[3] << 3 & 31 | g[4] >> 5)]
            e[j + 7] = a[(g[4] & 31)]
            j += 8
            i += 5

        return codecs.decode(e[:-padding], 'ASCII')

    def decode(self, e):
        r"""
        >>> import codecs
        >>> decode = standard.decode

        # >>> decode('222k62s62o')
        # '\x00\x01\x02\x03\x04\x05'
        # >>> decode('222k62s6')
        # '\x00\x01\x02\x03\x04'
        >>> codecs.decode(decode('zw'), 'unicode-escape')  # # doctest: +ALLOW_UNICODE
        '\xff'
        """
        n = len(e)
        m = old_div(n * 5, 8)
        padding = 5 - m % 5
        d = bytearray(m + padding)
        i, j = (0, 0)
        l = self.lookup
        while j < n:
            if n - j < 8:
                g = [ l[ord(x)] for x in e[j:] ] + [0] * (8 - (n - j))
            else:
                g = [ l[ord(x)] for x in e[j:j + 8] ]
            d[i + 0] = g[0] << 3 & 255 | g[1] >> 2
            d[i + 1] = g[1] << 6 & 255 | g[2] << 1 & 255 | g[3] >> 4
            d[i + 2] = g[3] << 4 & 255 | g[4] >> 1
            d[i + 3] = g[4] << 7 & 255 | g[5] << 2 & 255 | g[6] >> 3
            d[i + 4] = g[6] << 5 & 255 | g[7]
            j += 8
            i += 5

        return bytes(d[:-padding])


standard = D32('234567abcdefghijklmnopqrstuvwxyz')
base32 = D32('abcdefghijklmnopqrstuvwxyz234567')