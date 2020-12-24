# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Signature\test_pkcs1_15.py
# Compiled at: 2013-03-14 04:43:25
__revision__ = '$Id$'
import unittest
from Crypto.PublicKey import RSA
from Crypto.SelfTest.st_common import list_test_cases, a2b_hex, b2a_hex
from Crypto.Hash import *
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5 as PKCS
from Crypto.Util.py3compat import *

def isStr(s):
    t = ''
    try:
        t += s
    except TypeError:
        return 0

    return 1


def rws(t):
    """Remove white spaces, tabs, and new lines from a string"""
    for c in ['\n', '\t', ' ']:
        t = t.replace(c, '')

    return t


def t2b(t):
    """Convert a text string with bytes in hex form to a byte string"""
    clean = b(rws(t))
    if len(clean) % 2 == 1:
        raise ValueError('Even number of characters expected')
    return a2b_hex(clean)


class PKCS1_15_Tests(unittest.TestCase):
    _testData = (
     (
      {'n': '0a 66 79 1d c6 98 81 68 de 7a b7 74 19 bb 7f b0 c0 01 c6\n                    27 10 27 00 75 14 29 42 e1 9a 8d 8c 51 d0 53 b3 e3 78 2a 1d\n                    e5 dc 5a f4 eb e9 94 68 17 01 14 a1 df e6 7c dc 9a 9a f5 5d\n                    65 56 20 bb ab', 
         'e': '01 00\n                    01', 
         'd': '01 23 c5 b6 1b a3 6e db 1d 36 79 90 41 99 a8 9e a8 0c 09\n                    b9 12 2e 14 00 c0 9a dc f7 78 46 76 d0 1d 23 35 6a 7d 44 d6\n                    bd 8b d5 0e 94 bf c7 23 fa 87 d8 86 2b 75 17 76 91 c1 1d 75\n                    76 92 df 88 81'},
      '30 81 a4 02 01 00 30 42 31 0b 30 09 06\n                03 55 04 06 13 02 55 53 31 1d 30 1b 06 03 55 04 0a 13 14\n                45 78 61 6d 70 6c 65 20 4f 72 67 61 6e 69 7a 61 74 69 6f\n                6e 31 14 30 12 06 03 55 04 03 13 0b 54 65 73 74 20 55 73\n                65 72 20 31 30 5b 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01\n                05 00 03 4a 00 30 47 02 40\n                0a 66 79 1d c6 98 81 68 de 7a b7 74 19 bb 7f b0\n                c0 01 c6 27 10 27 00 75 14 29 42 e1 9a 8d 8c 51\n                d0 53 b3 e3 78 2a 1d e5 dc 5a f4 eb e9 94 68 17\n                01 14 a1 df e6 7c dc 9a 9a f5 5d 65 56 20 bb ab\n                02 03 01 00 01',
      '06 db 36 cb 18 d3 47 5b 9c 01 db 3c 78 95 28 08\n                02 79 bb ae ff 2b 7d 55 8e d6 61 59 87 c8 51 86\n                3f 8a 6c 2c ff bc 89 c3 f7 5a 18 d9 6b 12 7c 71\n                7d 54 d0 d8 04 8d a8 a0 54 46 26 d1 7a 2a 8f be',
      MD2),
     (
      '-----BEGIN RSA PRIVATE KEY-----\n                MIIBOwIBAAJBAL8eJ5AKoIsjURpcEoGubZMxLD7+kT+TLr7UkvEtFrRhDDKMtuII\n                q19FrL4pUIMymPMSLBn3hJLe30Dw48GQM4UCAwEAAQJACUSDEp8RTe32ftq8IwG8\n                Wojl5mAd1wFiIOrZ/Uv8b963WJOJiuQcVN29vxU5+My9GPZ7RA3hrDBEAoHUDPrI\n                OQIhAPIPLz4dphiD9imAkivY31Rc5AfHJiQRA7XixTcjEkojAiEAyh/pJHks/Mlr\n                +rdPNEpotBjfV4M4BkgGAA/ipcmaAjcCIQCHvhwwKVBLzzTscT2HeUdEeBMoiXXK\n                JACAr3sJQJGxIQIgarRp+m1WSKV1MciwMaTOnbU7wxFs9DP1pva76lYBzgUCIQC9\n                n0CnZCJ6IZYqSt0H5N7+Q+2Ro64nuwV/OSQfM6sBwQ==\n                -----END RSA PRIVATE KEY-----',
      'This is a test\n',
      '4a700a16432a291a3194646952687d5316458b8b86fb0a25aa30e0dcecdb\n                442676759ac63d56ec1499c3ae4c0013c2053cabd5b5804848994541ac16\n                fa243a4d',
      SHA1),
     (
      {'n': 'E08973398DD8F5F5E88776397F4EB005BB5383DE0FB7ABDC7DC775290D052E6D\n                    12DFA68626D4D26FAA5829FC97ECFA82510F3080BEB1509E4644F12CBBD832CF\n                    C6686F07D9B060ACBEEE34096A13F5F7050593DF5EBA3556D961FF197FC981E6\n                    F86CEA874070EFAC6D2C749F2DFA553AB9997702A648528C4EF357385774575F', 
         'e': '010001', 
         'd': '00A403C327477634346CA686B57949014B2E8AD2C862B2C7D748096A8B91F736\n                    F275D6E8CD15906027314735644D95CD6763CEB49F56AC2F376E1CEE0EBF282D\n                    F439906F34D86E085BD5656AD841F313D72D395EFE33CBFF29E4030B3D05A28F\n                    B7F18EA27637B07957D32F2BDE8706227D04665EC91BAF8B1AC3EC9144AB7F21'},
      'abc',
      '60AD5A78FB4A4030EC542C8974CD15F55384E836554CEDD9A322D5F4135C6267\n                A9D20970C54E6651070B0144D43844C899320DD8FA7819F7EBC6A7715287332E\n                C8675C136183B3F8A1F81EF969418267130A756FDBB2C71D9A667446E34E0EAD\n                9CF31BFB66F816F319D0B7E430A5F2891553986E003720261C7E9022C0D9F11F',
      SHA1))

    def testSign1(self):
        for i in range(len(self._testData)):
            row = self._testData[i]
            if isStr(row[0]):
                key = RSA.importKey(row[0])
            else:
                comps = [ long(rws(row[0][x]), 16) for x in ('n', 'e', 'd') ]
                key = RSA.construct(comps)
            h = row[3].new()
            try:
                h.update(t2b(row[1]))
            except:
                h.update(b(row[1]))

            signer = PKCS.new(key)
            self.failUnless(signer.can_sign())
            s = signer.sign(h)
            self.assertEqual(s, t2b(row[2]))

    def testVerify1(self):
        for i in range(len(self._testData)):
            row = self._testData[i]
            if isStr(row[0]):
                key = RSA.importKey(row[0]).publickey()
            else:
                comps = [ long(rws(row[0][x]), 16) for x in ('n', 'e') ]
                key = RSA.construct(comps)
            h = row[3].new()
            try:
                h.update(t2b(row[1]))
            except:
                h.update(b(row[1]))

            verifier = PKCS.new(key)
            self.failIf(verifier.can_sign())
            result = verifier.verify(h, t2b(row[2]))
            self.failUnless(result)

    def testSignVerify(self):
        rng = Random.new().read
        key = RSA.generate(1024, rng)
        for hashmod in (MD2, MD5, SHA1, SHA224, SHA256, SHA384, SHA512, RIPEMD160):
            h = hashmod.new()
            h.update(b('blah blah blah'))
            signer = PKCS.new(key)
            s = signer.sign(h)
            result = signer.verify(h, s)
            self.failUnless(result)


def get_tests(config={}):
    tests = []
    tests += list_test_cases(PKCS1_15_Tests)
    return tests


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')