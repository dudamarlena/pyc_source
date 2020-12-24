# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_SHA384.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Hash.SHA384"""
__revision__ = '$Id$'
test_data = [
 ('cb00753f45a35e8bb5a03d699ac65007272c32ab0eded1631a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7',
 'abc'),
 ('09330c33f71147e83d192fc782cd1b4753111b173b3b05d22fa08086e3b0f712fcc7c71a557e2db966c3e9fa91746039',
 'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu'),
 (
  '9d0e1809716474cb086e834e310a4a1ced149e9c00f248527972cec5704c2a5b07b8b3dc38ecc4ebae97ddd87f3d8985', 'a' * 1000000, "'a' * 10**6"),
 ('38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b',
 ''),
 ('71e8383a4cea32d6fd6877495db2ee353542f46fa44bc23100bca48f3366b84e809f0708e81041f427c6d5219a286677',
 'Franz jagt im komplett verwahrlosten Taxi quer durch Bayern')]

def get_tests(config={}):
    from Crypto.Hash import SHA384
    from common import make_hash_tests
    return make_hash_tests(SHA384, 'SHA384', test_data, digest_size=48, oid=b'\x06\t`\x86H\x01e\x03\x04\x02\x02')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')