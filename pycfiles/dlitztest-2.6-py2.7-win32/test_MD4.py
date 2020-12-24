# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_MD4.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Hash.MD4"""
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('31d6cfe0d16ae931b73c59d7e0c089c0', '', "'' (empty string)"),
 ('bde52cb31de33e46245e05fbdbd6fb24', 'a'),
 ('a448017aaf21d8525fc10ae87aa6729d', 'abc'),
 ('d9130a8164549fe818874806e1c7014b', 'message digest'),
 ('d79e1c308aa5bbcdeea8ed63df412da9', 'abcdefghijklmnopqrstuvwxyz', 'a-z'),
 ('043f8582f241db351ce627e153e7f0e4', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
 'A-Z, a-z, 0-9'),
 (
  'e33b4ddc9c38f2199c3e7b164fcc0536',
  '1234567890123456789012345678901234567890123456' + '7890123456789012345678901234567890',
  "'1234567890' * 8")]

def get_tests(config={}):
    from Crypto.Hash import MD4
    from common import make_hash_tests
    return make_hash_tests(MD4, 'MD4', test_data, digest_size=16, oid=b'\x06\x08*\x86H\x86\xf7\r\x02\x04')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')