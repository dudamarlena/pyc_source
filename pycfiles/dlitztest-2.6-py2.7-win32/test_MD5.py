# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_MD5.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Hash.MD5"""
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('d41d8cd98f00b204e9800998ecf8427e', '', "'' (empty string)"),
 ('0cc175b9c0f1b6a831c399e269772661', 'a'),
 ('900150983cd24fb0d6963f7d28e17f72', 'abc'),
 ('f96b697d7cb7938d525a2f31aaf161d0', 'message digest'),
 ('c3fcd3d76192e4007dfb496cca67e13b', 'abcdefghijklmnopqrstuvwxyz', 'a-z'),
 ('d174ab98d277d9f5a5611c2c9f419d9f', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
 'A-Z, a-z, 0-9'),
 (
  '57edf4a22be3c955ac49da2e2107b67a',
  '1234567890123456789012345678901234567890123456' + '7890123456789012345678901234567890',
  "'1234567890' * 8")]

def get_tests(config={}):
    from Crypto.Hash import MD5
    from common import make_hash_tests
    return make_hash_tests(MD5, 'MD5', test_data, digest_size=16, oid=b'\x06\x08*\x86H\x86\xf7\r\x02\x05')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')