# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_RIPEMD160.py
# Compiled at: 2013-03-14 04:43:25
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('9c1185a5c5e9fc54612808977ee8f548b2258d31', '', "'' (empty string)"),
 ('0bdc9d2d256b3ee9daae347be6f4dc835a467ffe', 'a'),
 ('8eb208f7e05d987a9b044a8e98c6b087f15a0bfc', 'abc'),
 ('5d0689ef49d2fae572b881b123a85ffa21595f36', 'message digest'),
 ('f71c27109c692c1b56bbdceb5b9d2865b3708dbc', 'abcdefghijklmnopqrstuvwxyz', 'a-z'),
 ('12a053384a9c0c88e405a06c27dcf49ada62eb2b', 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
 'abcdbcd...pnopq'),
 ('b0e20b6e3116640286ed3a87a5713079b21f5189', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
 'A-Z, a-z, 0-9'),
 (
  '9b752e45573d4b39f4dbd3323cab82bf63326bfb',
  '1234567890' * 8,
  "'1234567890' * 8"),
 (
  '52783243c1697bdbe16d37f97f68f08325dc1528',
  'a' * 1000000,
  '"a" * 10**6')]

def get_tests(config={}):
    from Crypto.Hash import RIPEMD160
    from common import make_hash_tests
    return make_hash_tests(RIPEMD160, 'RIPEMD160', test_data, digest_size=20, oid='\x06\x05+$\x03\x02\x01')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')