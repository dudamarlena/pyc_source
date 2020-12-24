# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_SHA256.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Hash.SHA256"""
__revision__ = '$Id$'
import unittest
from Crypto.Util.py3compat import *

class LargeSHA256Test(unittest.TestCase):

    def runTest(self):
        """SHA256: 512/520 MiB test"""
        from Crypto.Hash import SHA256
        zeros = bchr(0) * 1048576
        h = SHA256.new(zeros)
        for i in xrange(511):
            h.update(zeros)

        self.assertEqual('9acca8e8c22201155389f65abbf6bc9723edc7384ead80503839f49dcc56d767', h.hexdigest())
        for i in xrange(8):
            h.update(zeros)

        self.assertEqual('abf51ad954b246009dfe5a50ecd582fd5b8f1b8b27f30393853c3ef721e7fa6e', h.hexdigest())


def get_tests(config={}):
    test_data = [
     ('ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad', 'abc'),
     ('248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1', 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'),
     (
      'cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0',
      'a' * 1000000,
      '"a" * 10**6'),
     ('f7fd017a3c721ce7ff03f3552c0813adcc48b7f33f07e5e2ba71e23ea393d103', 'This message is precisely 55 bytes long, to test a bug.',
 'Length = 55 (mod 64)'),
     ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', ''),
     ('d32b568cd1b96d459e7291ebf4b25d007f275c9f13149beeb782fac0716613f8', 'Franz jagt im komplett verwahrlosten Taxi quer durch Bayern')]
    from Crypto.Hash import SHA256
    from common import make_hash_tests
    tests = make_hash_tests(SHA256, 'SHA256', test_data, digest_size=32, oid=b'\x06\t`\x86H\x01e\x03\x04\x02\x01')
    if config.get('slow_tests'):
        tests += [LargeSHA256Test()]
    return tests


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')