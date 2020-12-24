# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_SHA224.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Hash.SHA224"""
__revision__ = '$Id$'
test_data = [
 ('23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7', 'abc'),
 ('75388b16512776cc5dba5da1fd890150b0c6455cb4f58b1952522525', 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'),
 (
  '20794655980c91d8bbb4c1ea97618a4bf03f42581948b2ee4ee7ad67', 'a' * 1000000, "'a' * 10**6"),
 ('d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f', ''),
 ('49b08defa65e644cbf8a2dd9270bdededabc741997d1dadd42026d7b', 'Franz jagt im komplett verwahrlosten Taxi quer durch Bayern'),
 ('58911e7fccf2971a7d07f93162d8bd13568e71aa8fc86fc1fe9043d1', 'Frank jagt im komplett verwahrlosten Taxi quer durch Bayern')]

def get_tests(config={}):
    from Crypto.Hash import SHA224
    from common import make_hash_tests
    return make_hash_tests(SHA224, 'SHA224', test_data, digest_size=28, oid=b'\x06\t`\x86H\x01e\x03\x04\x02\x04')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')