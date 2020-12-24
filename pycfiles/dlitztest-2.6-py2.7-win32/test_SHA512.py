# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_SHA512.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Hash.SHA512"""
__revision__ = '$Id$'
test_data = [
 ('ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f',
 'abc'),
 ('8e959b75dae313da8cf4f72814fc143f8f7779c6eb9f7fa17299aeadb6889018501d289e4900f7e4331b99dec4b5433ac7d329eeb6dd26545e96e55b874be909',
 'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu'),
 (
  'e718483d0ce769644e2e42c7bc15b4638e1f98b13b2044285632a803afa973ebde0ff244877ea60a4cb0432ce577c31beb009c5c2c49aa2e4eadb217ad8cc09b', 'a' * 1000000, "'a' * 10**6"),
 ('cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
 ''),
 ('af9ed2de700433b803240a552b41b5a472a6ef3fe1431a722b2063c75e9f07451f67a28e37d09cde769424c96aea6f8971389db9e1993d6c565c3c71b855723c',
 'Franz jagt im komplett verwahrlosten Taxi quer durch Bayern')]

def get_tests(config={}):
    from Crypto.Hash import SHA512
    from common import make_hash_tests
    return make_hash_tests(SHA512, 'SHA512', test_data, digest_size=64, oid=b'\x06\t`\x86H\x01e\x03\x04\x02\x03')


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')