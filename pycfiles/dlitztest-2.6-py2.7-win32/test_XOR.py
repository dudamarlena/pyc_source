# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Cipher\test_XOR.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Cipher.XOR"""
import unittest
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('01', '01', '00', 'zero key'),
 ('0102040810204080', '0003050911214181', '01', '1-byte key'),
 ('0102040810204080', 'cda8c8a2dc8a8c2a', 'ccaa', '2-byte key'),
 (
  'ff' * 64, 'fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0efeeedecebeae9e8e7e6e5e4e3e2e1e0' * 2,
  '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f',
  '32-byte key')]

class TruncationSelfTest(unittest.TestCase):

    def runTest(self):
        """33-byte key (should raise ValueError under current implementation)"""
        self.assertRaises(ValueError, XOR.new, 'x' * 33)


def get_tests(config={}):
    global XOR
    from Crypto.Cipher import XOR
    from common import make_stream_tests
    return make_stream_tests(XOR, 'XOR', test_data) + [TruncationSelfTest()]


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')