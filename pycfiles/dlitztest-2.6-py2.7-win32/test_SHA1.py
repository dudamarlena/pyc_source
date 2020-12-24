# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_SHA1.py
# Compiled at: 2013-03-14 04:43:25
"""Self-test suite for Crypto.Hash.SHA"""
__revision__ = '$Id$'
from Crypto.Util.py3compat import *
test_data = [
 ('a9993e364706816aba3e25717850c26c9cd0d89d', 'abc'),
 ('84983e441c3bd26ebaae4aa1f95129e5e54670f1', 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'),
 (
  'dea356a2cddd90c7a7ecedc5ebb563934f460452',
  '01234567' * 80,
  '"01234567" * 80')]

def get_tests(config={}):
    from Crypto.Hash import SHA1
    from common import make_hash_tests
    return make_hash_tests(SHA1, 'SHA1', test_data, digest_size=20, oid='\x06\x05+\x0e\x03\x02\x1a')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')