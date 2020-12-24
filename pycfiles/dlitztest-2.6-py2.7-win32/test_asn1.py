# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Util\test_asn1.py
# Compiled at: 2013-03-14 04:43:25
"""Self-tests for Crypto.Util.asn1"""
__revision__ = '$Id$'
import unittest, sys
from Crypto.Util.py3compat import *
from Crypto.Util.asn1 import DerSequence, DerObject

class DerObjectTests(unittest.TestCase):

    def testObjEncode1(self):
        der = DerObject(b('3'))
        self.assertEquals(der.encode(), b('3\x00'))
        der.payload = b('E')
        self.assertEquals(der.encode(), b('3\x01E'))
        self.assertEquals(der.encode(), b('3\x01E'))
        der = DerObject(b(51))
        der.payload = b('E')
        self.assertEquals(der.encode(), b('3\x01E'))

    def testObjEncode2(self):
        der = DerObject('SEQUENCE')
        self.assertEquals(der.encode(), b('0\x00'))
        der = DerObject('BIT STRING')
        self.assertEquals(der.encode(), b('\x03\x00'))

    def testObjEncode3(self):
        der = DerObject(b('4'))
        der.payload = b('0') * 128
        self.assertEquals(der.encode(), b(b'4\x81\x80' + '0' * 128))

    def testObjDecode1(self):
        der = DerObject()
        der.decode(b(' \x02\x01\x02'))
        self.assertEquals(der.payload, b('\x01\x02'))
        self.assertEquals(der.typeTag, 32)

    def testObjDecode2(self):
        der = DerObject()
        der.decode(b(b'"\x81\x80' + '1' * 128))
        self.assertEquals(der.payload, b('1') * 128)
        self.assertEquals(der.typeTag, 34)


class DerSequenceTests(unittest.TestCase):

    def testEncode1(self):
        der = DerSequence()
        self.assertEquals(der.encode(), b('0\x00'))
        self.failIf(der.hasOnlyInts())
        der.append(0)
        self.assertEquals(der.encode(), b('0\x03\x02\x01\x00'))
        self.failUnless(der.hasOnlyInts())
        self.assertEquals(der.encode(), b('0\x03\x02\x01\x00'))

    def testEncode2(self):
        der = DerSequence()
        der.append(127)
        self.assertEquals(der.encode(), b('0\x03\x02\x01\x7f'))
        der[0] = 1
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 1)
        self.assertEquals(der[(-1)], 1)
        self.assertEquals(der.encode(), b('0\x03\x02\x01\x01'))
        der[:] = [
         1]
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 1)
        self.assertEquals(der.encode(), b('0\x03\x02\x01\x01'))

    def testEncode3(self):
        der = DerSequence()
        der.append(384)
        self.assertEquals(der.encode(), b(b'0\x04\x02\x02\x01\x80'))

    def testEncode4(self):
        der = DerSequence()
        der.append(32317006071311007300714876688669951960444102669715484032130345427524655138867890893197201411522913463688717960921898019494119559150490921095088152386448283120630877367300996091750197750389652106796057638384067568276792218642619756161838094338476170470581645852036305042887575891541065808607552399123930385521914333389668342420684974786564569494856176035326322058077805659331026192708460314150258592864177116725943603718461857357598351152301645904403697613233287231227125684710820209725157101726931323469678542580656697935045997268352998638215525166389437335543602135433229604645318478604952148193555853611059596230656)
        self.assertEquals(der.encode(), b(b'0\x82\x01\x05') + b(b'\x02\x82\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    def testEncode5(self):
        der = DerSequence()
        der.append(255)
        self.assertEquals(der.encode(), b(b'0\x04\x02\x02\x00\xff'))

    def testEncode6(self):
        der = DerSequence()
        der.append(384)
        der.append(255)
        self.assertEquals(der.encode(), b(b'0\x08\x02\x02\x01\x80\x02\x02\x00\xff'))
        self.failUnless(der.hasOnlyInts())
        der.append(1)
        der[1:] = [9, 8]
        self.assertEquals(len(der), 3)
        self.assertEqual(der[1:], [9, 8])
        self.assertEqual(der[1:-1], [9])
        self.assertEquals(der.encode(), b(b'0\n\x02\x02\x01\x80\x02\x01\t\x02\x01\x08'))

    def testEncode7(self):
        der = DerSequence()
        der.append(384)
        der.append(b('\x00\x02\x00\x00'))
        self.assertEquals(der.encode(), b(b'0\x08\x02\x02\x01\x80\x00\x02\x00\x00'))
        self.failIf(der.hasOnlyInts())

    def testDecode1(self):
        der = DerSequence()
        der.decode(b('0\x00'))
        self.assertEquals(len(der), 0)
        der.decode(b('0\x03\x02\x01\x00'))
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 0)
        der.decode(b('0\x03\x02\x01\x00'))
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 0)

    def testDecode2(self):
        der = DerSequence()
        der.decode(b('0\x03\x02\x01\x7f'))
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 127)

    def testDecode3(self):
        der = DerSequence()
        der.decode(b(b'0\x04\x02\x02\x01\x80'))
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 384)

    def testDecode4(self):
        der = DerSequence()
        der.decode(b(b'0\x82\x01\x05') + b(b'\x02\x82\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') + b('\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 32317006071311007300714876688669951960444102669715484032130345427524655138867890893197201411522913463688717960921898019494119559150490921095088152386448283120630877367300996091750197750389652106796057638384067568276792218642619756161838094338476170470581645852036305042887575891541065808607552399123930385521914333389668342420684974786564569494856176035326322058077805659331026192708460314150258592864177116725943603718461857357598351152301645904403697613233287231227125684710820209725157101726931323469678542580656697935045997268352998638215525166389437335543602135433229604645318478604952148193555853611059596230656)

    def testDecode5(self):
        der = DerSequence()
        der.decode(b(b'0\x04\x02\x02\x00\xff'))
        self.assertEquals(len(der), 1)
        self.assertEquals(der[0], 255)

    def testDecode6(self):
        der = DerSequence()
        der.decode(b(b'0\x08\x02\x02\x01\x80\x02\x02\x00\xff'))
        self.assertEquals(len(der), 2)
        self.assertEquals(der[0], 384)
        self.assertEquals(der[1], 255)

    def testDecode7(self):
        der = DerSequence()
        der.decode(b(b'0\n\x02\x02\x01\x80$\x02\xb6c\x12\x00'))
        self.assertEquals(len(der), 3)
        self.assertEquals(der[0], 384)
        self.assertEquals(der[1], b(b'$\x02\xb6c'))
        self.assertEquals(der[2], b('\x12\x00'))

    def testDecode8(self):
        der = DerSequence()
        der.decode(b(b'0\x06$\x02\xb6c\x12\x00'))
        self.assertEquals(len(der), 2)
        self.assertEquals(der[0], b(b'$\x02\xb6c'))
        self.assertEquals(der[1], b('\x12\x00'))

    def testErrDecode1(self):
        der = DerSequence()
        self.assertRaises(ValueError, der.decode, b(''))
        self.assertRaises(ValueError, der.decode, b('\x00'))
        self.assertRaises(ValueError, der.decode, b('0'))

    def testErrDecode2(self):
        der = DerSequence()
        self.assertRaises(ValueError, der.decode, b('0\x00\x00'), True)

    def testErrDecode3(self):
        der = DerSequence()
        self.assertRaises(ValueError, der.decode, b('0\x04\x02\x01\x01\x00'))
        self.assertRaises(ValueError, der.decode, b(b'0\x81\x03\x02\x01\x01'))
        self.assertRaises(ValueError, der.decode, b(b'0\x04\x02\x81\x01\x01'))

    def testErrDecode4(self):
        der = DerSequence()
        self.assertRaises(ValueError, der.decode, b(b'0\x04\x02\x01\xff'))


def get_tests(config={}):
    from Crypto.SelfTest.st_common import list_test_cases
    listTests = []
    listTests += list_test_cases(DerObjectTests)
    listTests += list_test_cases(DerSequenceTests)
    return listTests


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')