# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/out_of_shape/test_zlibutil.py
# Compiled at: 2018-01-06 14:43:43
import unittest
from pyutil import randutil
from pyutil import zlibutil

class Accumulator:

    def __init__(self):
        self.buf = ''

    def write(self, str):
        self.buf += str


def make_decomp(realdecomp):

    def decomp(str, maxlen, maxmem):
        d = Accumulator()
        realdecomp(str, d, maxlen, maxmem)
        return d.buf

    return decomp


def genrandstr(strlen):
    return randutil.insecurerandstr(strlen)


def genbombstr(strlen):
    return '0' * strlen


MAXMEM = 65 * 1048576

class ZlibTestCase(unittest.TestCase):

    def _help_test(self, genstring, decomp, strlen):
        s = genstring(strlen)
        cs = zlibutil.zlib.compress(s)
        s2 = decomp(cs, maxlen=strlen, maxmem=strlen * 8 + zlibutil.MINMAXMEM)
        self.failUnless(s == s2)
        s2 = decomp(cs, maxlen=strlen, maxmem=strlen * 64 + zlibutil.MINMAXMEM)
        self.failUnless(s == s2)
        self.failUnlessRaises(zlibutil.TooBigError, decomp, cs, maxlen=strlen - 1, maxmem=strlen * 8 + zlibutil.MINMAXMEM)

    def _help_test_inplace_minmaxmem(self, genstring, decomp, strlen):
        s = genstring(strlen)
        cs = zlibutil.zlib.compress(s)
        s2 = decomp(cs, maxlen=strlen, maxmem=zlibutil.MINMAXMEM)
        self.failUnless(s == s2)
        self.failUnlessRaises(zlibutil.TooBigError, decomp, cs, maxlen=strlen - 1, maxmem=zlibutil.MINMAXMEM)

    def _help_test_inplace(self, genstring, decomp, strlen):
        s = genstring(strlen)
        cs = zlibutil.zlib.compress(s)
        s2 = decomp(cs, maxlen=strlen, maxmem=max(strlen * 8, zlibutil.MINMAXMEM))
        self.failUnless(s == s2)
        s2 = decomp(cs, maxlen=strlen, maxmem=max(strlen * 64, zlibutil.MINMAXMEM))
        self.failUnless(s == s2)
        s2 = decomp(cs, maxlen=strlen, maxmem=max(strlen - 1, zlibutil.MINMAXMEM))
        self.failUnless(s == s2)
        s2 = decomp(cs, maxlen=strlen, maxmem=max(strlen / 2, zlibutil.MINMAXMEM))
        self.failUnless(s == s2)
        self.failUnlessRaises(zlibutil.TooBigError, decomp, cs, maxlen=strlen - 1, maxmem=max(strlen * 8, zlibutil.MINMAXMEM))

    def testem(self):
        for strlen in [2, 3, 4, 99]:
            for decomp in [zlibutil.decompress, make_decomp(zlibutil.decompress_to_fileobj), make_decomp(zlibutil.decompress_to_spool)]:
                for genstring in [genrandstr, genbombstr]:
                    self._help_test(genstring, decomp, strlen)

            for decomp in [make_decomp(zlibutil.decompress_to_spool)]:
                for genstring in [genrandstr, genbombstr]:
                    self._help_test_inplace(genstring, decomp, strlen)
                    self._help_test_inplace_minmaxmem(genstring, decomp, strlen)