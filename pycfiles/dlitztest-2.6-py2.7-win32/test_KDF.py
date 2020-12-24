# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Protocol\test_KDF.py
# Compiled at: 2013-03-14 04:43:25
__revision__ = '$Id$'
import unittest
from binascii import unhexlify
from Crypto.SelfTest.st_common import list_test_cases
from Crypto.Hash import SHA1, HMAC
from Crypto.Protocol.KDF import *

def t2b(t):
    return unhexlify(b(t))


class PBKDF1_Tests(unittest.TestCase):
    _testData = (('password', '78578E5A5D63CB06', 16, 1000, 'DC19847E05C64D2FAF10EBFB4A3D2A20'), )

    def test1(self):
        v = self._testData[0]
        res = PBKDF1(v[0], t2b(v[1]), v[2], v[3], SHA1)
        self.assertEqual(res, t2b(v[4]))


class PBKDF2_Tests(unittest.TestCase):
    _testData = (
     ('password', '78578E5A5D63CB06', 24, 2048, 'BFDE6BE94DF7E11DD409BCE20A0255EC327CB936FFE93643'),
     ('password', '73616c74', 20, 1, '0c60c80f961f0e71f3a9b524af6012062fe037a6'),
     ('password', '73616c74', 20, 2, 'ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957'),
     ('password', '73616c74', 20, 4096, '4b007901b765489abead49d926f721d065a429c1'),
     ('passwordPASSWORDpassword', '73616c7453414c5473616c7453414c5473616c7453414c5473616c7453414c5473616c74',
 25, 4096, '3d2eec4fe41c849b80c8d83662c0e44a8b291a964cf2f07038'),
     ('pass\x00word', '7361006c74', 16, 4096, '56fa6aa75548099dcc37d7f03425e0c3'))

    def test1(self):

        def prf(p, s):
            return HMAC.new(p, s, SHA1).digest()

        for i in xrange(len(self._testData)):
            v = self._testData[i]
            res = PBKDF2(v[0], t2b(v[1]), v[2], v[3])
            res2 = PBKDF2(v[0], t2b(v[1]), v[2], v[3], prf)
            self.assertEqual(res, t2b(v[4]))
            self.assertEqual(res, res2)


def get_tests(config={}):
    tests = []
    tests += list_test_cases(PBKDF1_Tests)
    tests += list_test_cases(PBKDF2_Tests)
    return tests


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')