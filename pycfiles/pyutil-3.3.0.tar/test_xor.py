# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/deprecated/test_xor.py
# Compiled at: 2018-01-06 14:43:43
import unittest
from pyutil.xor import xor

def _help_test(xf):
    assert xf('\x00', '\x00') == '\x00'
    assert xf('\x01', '\x00') == '\x01'
    assert xf('\x01', '\x01') == '\x00'
    assert xf('\x00\x01', '\x00\x01') == '\x00\x00'
    assert xf('@A', '\x00A') == '@\x00'


class Testy(unittest.TestCase):

    def test_em(self):
        for xorfunc in (xor.py_xor, xor.py_xor_simple, xor.xor):
            if callable(xorfunc):
                _help_test(xorfunc)