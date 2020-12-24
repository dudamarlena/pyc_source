# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Cipher\test_CAST.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Cipher.CAST"""
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('0123456789abcdef', '238b4fe5847e44b2', '0123456712345678234567893456789a', '128-bit key'),
 ('0123456789abcdef', 'eb6a711a2c02271b', '01234567123456782345', '80-bit key'),
 ('0123456789abcdef', '7ac816d16e9b302e', '0123456712', '40-bit key')]

def get_tests(config={}):
    from Crypto.Cipher import CAST
    from common import make_block_tests
    return make_block_tests(CAST, 'CAST', test_data)


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')