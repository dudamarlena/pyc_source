# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_MD2.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Hash.MD2"""
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('8350e5a3e24c153df2275c9f80692773', '', "'' (empty string)"),
 ('32ec01ec4a6dac72c0ab96fb34c0b5d1', 'a'),
 ('da853b0d3f88d99b30283a69e6ded6bb', 'abc'),
 ('ab4f496bfb2a530b219ff33031fe06b0', 'message digest'),
 ('4e8ddff3650292ab5a4108c3aa47940b', 'abcdefghijklmnopqrstuvwxyz', 'a-z'),
 ('da33def2a42df13975352846c30338cd', 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
 'A-Z, a-z, 0-9'),
 (
  'd5976f79d83d3a0dc9806c3c66f3efd8',
  '1234567890123456789012345678901234567890123456' + '7890123456789012345678901234567890',
  "'1234567890' * 8")]

def get_tests(config={}):
    from Crypto.Hash import MD2
    from common import make_hash_tests
    return make_hash_tests(MD2, 'MD2', test_data, digest_size=16, oid=b'\x06\x08*\x86H\x86\xf7\r\x02\x02')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')