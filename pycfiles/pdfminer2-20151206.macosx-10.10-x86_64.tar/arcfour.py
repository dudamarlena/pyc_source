# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/arcfour.py
# Compiled at: 2015-10-31 16:12:15
""" Python implementation of Arcfour encryption algorithm.
See https://en.wikipedia.org/wiki/RC4
This code is in the public domain.

"""
import six

class Arcfour(object):

    def __init__(self, key):
        s = [ i for i in range(256) ]
        j = 0
        klen = len(key)
        for i in range(256):
            j = (j + s[i] + six.indexbytes(key, i % klen)) % 256
            s[i], s[j] = s[j], s[i]

        self.s = s
        self.i, self.j = (0, 0)

    def process(self, data):
        i, j = self.i, self.j
        s = self.s
        r = ''
        for c in six.iterbytes(data):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            s[i], s[j] = s[j], s[i]
            k = s[((s[i] + s[j]) % 256)]
            r += six.int2byte(c ^ k)

        self.i, self.j = i, j
        return r

    encrypt = decrypt = process


new = Arcfour