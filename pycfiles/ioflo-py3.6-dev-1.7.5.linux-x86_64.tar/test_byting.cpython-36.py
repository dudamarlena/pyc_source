# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aid/test/test_byting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 17016 bytes
"""
Unit Test Template
"""
from __future__ import absolute_import, division, print_function
import sys, datetime
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os
from ioflo.aid.sixing import *
from ioflo.aid.odicting import odict
from ioflo.test import testing
from ioflo.aid.consoling import getConsole
console = getConsole()
from ioflo.aid import byting

def setUpModule():
    console.reinit(verbosity=(console.Wordage.concise))


def tearDownModule():
    pass


class BasicTestCase(unittest.TestCase):
    __doc__ = '\n    Example TestCase\n    '

    def setUp(self):
        super(BasicTestCase, self).setUp()

    def tearDown(self):
        super(BasicTestCase, self).tearDown()

    def testBinizeUnbinize(self):
        """
        Test the binize unbinize functions
        """
        console.terse('{0}\n'.format(self.testBinizeUnbinize.__doc__))
        n = 5
        u = byting.binize(n, 8)
        self.assertEqual(u, '00000101')
        n = byting.unbinize(u)
        self.assertEqual(n, 5)

    def testBytifyUnbytify(self):
        """
        Test the bytify unbytify functions
        """
        console.terse('{0}\n'.format(self.testBytifyUnbytify.__doc__))
        b = bytearray([1, 2, 3])
        n = byting.unbytify(b)
        self.assertEqual(n, 66051)
        n = byting.unbytify([1, 2, 3])
        self.assertEqual(n, 66051)
        n = byting.unbytify(b'\x01\x02\x03')
        self.assertEqual(n, 66051)
        b = byting.bytify(n)
        self.assertEqual(b, bytearray([1, 2, 3]))
        b = byting.bytify(n, 4)
        self.assertEqual(b, bytearray([0, 1, 2, 3]))
        b = byting.bytify(n, 2)
        self.assertEqual(b, bytearray([1, 2, 3]))
        b = byting.bytify(n, 2, strict=True)
        self.assertEqual(b, bytearray([2, 3]))
        b = bytearray([1, 2, 3])
        n = byting.unbytify(b, reverse=True)
        self.assertEqual(n, 197121)
        n = byting.unbytify([1, 2, 3], reverse=True)
        self.assertEqual(n, 197121)
        n = byting.unbytify(b'\x01\x02\x03', reverse=True)
        self.assertEqual(n, 197121)
        b = byting.bytify(n, reverse=True)
        self.assertEqual(b, bytearray([1, 2, 3]))
        b = byting.bytify(n, 4, reverse=True)
        self.assertEqual(b, bytearray([1, 2, 3, 0]))
        b = byting.bytify(n, 2, reverse=True)
        self.assertEqual(b, bytearray([1, 2, 3]))
        b = byting.bytify(n, 2, reverse=True, strict=True)
        self.assertEqual(b, bytearray([1, 2]))
        n = -1
        b = byting.bytify(n)
        self.assertEqual(b, bytearray([255]))
        b = byting.bytify(n, 4)
        self.assertEqual(b, bytearray([255, 255, 255, 255]))
        n = -2
        b = byting.bytify(n)
        self.assertEqual(b, bytearray([254]))
        b = byting.bytify(n, 2)
        self.assertEqual(b, bytearray([255, 254]))
        n = 32763
        b = byting.bytify(n, 3)
        self.assertEqual(b, bytearray([0, 127, 251]))
        b = byting.bytify(n, 3, reverse=True)
        self.assertEqual(b, bytearray([251, 127, 0]))

    def testPackifyUnpackify(self):
        """
        Test the packbits
        """
        console.terse('{0}\n'.format(self.testPackifyUnpackify.__doc__))
        fmt = '3 2 1 1'
        fields = [6, 2, True, False]
        size = 1
        packed = byting.packify(fmt=fmt, fields=fields, size=size)
        self.assertEqual(packed, bytearray([212]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '11010100')
        packed = byting.packify(fmt=fmt, fields=fields)
        self.assertEqual(packed, bytearray([212]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '11010100')
        fmt = ''
        fields = []
        size = 0
        packed = byting.packify(fmt=fmt, fields=fields, size=size)
        self.assertEqual(packed, bytearray([]))
        packed = byting.packify(fmt=fmt, fields=fields)
        self.assertEqual(packed, bytearray([]))
        fmt = '3 1'
        fields = [5, True]
        size = 1
        packed = byting.packify(fmt=fmt, fields=fields, size=size)
        self.assertEqual(packed, bytearray([176]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '10110000')
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = 3
        packed = byting.packify(fmt=fmt, fields=fields, size=size)
        self.assertEqual(packed, bytearray([165, 224, 65]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '101001011110000001000001')
        packed = byting.packify(fmt=fmt, fields=fields)
        self.assertEqual(packed, bytearray([165, 224, 65]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '101001011110000001000001')
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = 4
        packed = byting.packify(fmt=fmt, fields=fields, size=size)
        self.assertEqual(packed, bytearray([165, 224, 65, 0]))
        fmt = '3 2 1 1'
        packed = bytearray([212])
        fields = byting.unpackify(fmt=fmt, b=packed, boolean=True)
        self.assertEqual(fields, (6, 2, True, False, False))
        fields = byting.unpackify(fmt=fmt, b=packed, boolean=False)
        self.assertEqual(fields, (6, 2, 1, 0, 0))
        fmt = ''
        packed = bytearray([])
        fields = byting.unpackify(fmt=fmt, b=packed)
        self.assertEqual(fields, tuple())
        fmt = '3 1'
        packed = bytearray([176])
        fields = byting.unpackify(fmt=fmt, b=packed)
        self.assertEqual(fields, (5, 1, 0))
        fmt = '4 3 1'
        packed = [11]
        fields = byting.unpackify(fmt=fmt, b=packed)
        self.assertEqual(fields, (0, 5, 1))
        fmt = '8 6 7 3'
        packed = bytearray([165, 224, 65])
        fields = byting.unpackify(fmt=fmt, b=packed)
        self.assertEqual(fields, (165, 56, 8, 1))
        fmt = '8 6 7 3'
        packed = bytearray([165, 224, 65, 255, 255])
        fields = byting.unpackify(fmt=fmt, b=packed, size=3)
        self.assertEqual(fields, (165, 56, 8, 1))
        fmt = '3 2 1 1'
        fields = [6, 2, True, False]
        size = 1
        packed = byting.packify(fmt=fmt, fields=fields, size=size, reverse=True)
        self.assertEqual(packed, bytearray([212]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '11010100')
        packed = byting.packify(fmt=fmt, fields=fields, reverse=True)
        self.assertEqual(packed, bytearray([212]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '11010100')
        fmt = ''
        fields = []
        size = 0
        packed = byting.packify(fmt=fmt, fields=fields, size=size, reverse=True)
        self.assertEqual(packed, bytearray([]))
        packed = byting.packify(fmt=fmt, fields=fields, reverse=True)
        self.assertEqual(packed, bytearray([]))
        fmt = '3 1'
        fields = [5, True]
        size = 1
        packed = byting.packify(fmt=fmt, fields=fields, size=size, reverse=True)
        self.assertEqual(packed, bytearray([176]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '10110000')
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = 3
        packed = byting.packify(fmt=fmt, fields=fields, size=size, reverse=True)
        self.assertEqual(packed, bytearray([65, 224, 165]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '010000011110000010100101')
        packed = byting.packify(fmt=fmt, fields=fields, reverse=True)
        self.assertEqual(packed, bytearray([65, 224, 165]))
        self.assertEqual(byting.binize(byting.unbytify(packed), size * 8), '010000011110000010100101')
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = 4
        packed = byting.packify(fmt=fmt, fields=fields, size=size, reverse=True)
        self.assertEqual(packed, bytearray([0, 65, 224, 165]))
        fmt = '3 2 1 1'
        packed = bytearray([212])
        fields = byting.unpackify(fmt=fmt, b=packed, boolean=True, reverse=True)
        self.assertEqual(fields, (6, 2, True, False, False))
        fields = byting.unpackify(fmt=fmt, b=packed, boolean=False, reverse=True)
        self.assertEqual(fields, (6, 2, 1, 0, 0))
        fmt = ''
        packed = bytearray([])
        fields = byting.unpackify(fmt=fmt, b=packed, reverse=True)
        self.assertEqual(fields, tuple())
        fmt = '3 1'
        packed = bytearray([176])
        fields = byting.unpackify(fmt=fmt, b=packed, reverse=True)
        self.assertEqual(fields, (5, 1, 0))
        fmt = '4 3 1'
        packed = [11]
        fields = byting.unpackify(fmt=fmt, b=packed, reverse=True)
        self.assertEqual(fields, (0, 5, 1))
        fmt = '8 6 7 3'
        packed = bytearray([165, 224, 65])
        fields = byting.unpackify(fmt=fmt, b=packed, reverse=True)
        self.assertEqual(fields, (65, 56, 20, 5))
        fmt = '8 6 7 3'
        packed = bytearray([255, 255, 165, 224, 65])
        fields = byting.unpackify(fmt=fmt, b=packed, size=3, reverse=True)
        self.assertEqual(fields, (65, 56, 20, 5))

    def testPackifyInto(self):
        """
        Test the packbits
        """
        console.terse('{0}\n'.format(self.testPackifyInto.__doc__))
        fmt = '3 2 1 1'
        fields = [6, 2, True, False]
        b = bytearray([0, 0, 0, 0, 0, 0])
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=1)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([212, 0, 0, 0, 0, 0]))
        self.assertEqual(byting.binize(b[0]), '11010100')
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=1, offset=2)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([212, 0, 212, 0, 0, 0]))
        self.assertEqual(byting.binize(b[2]), '11010100')
        b[0] = 0
        self.assertEqual(b, bytearray([0, 0, 212, 0, 0, 0]))
        size = byting.packifyInto(b, fmt=fmt, fields=fields)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([212, 0, 212, 0, 0, 0]))
        self.assertEqual(byting.binize(b[0]), '11010100')
        b = bytearray([0, 0, 0, 0, 0, 0])
        fmt = ''
        fields = []
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=0)
        self.assertEqual(size, 0)
        self.assertEqual(b, bytearray([0, 0, 0, 0, 0, 0]))
        size = byting.packifyInto(b, fmt=fmt, fields=fields)
        self.assertEqual(size, 0)
        self.assertEqual(b, bytearray([0, 0, 0, 0, 0, 0]))
        fmt = '3 1'
        fields = [5, True]
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=1)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([176, 0, 0, 0, 0, 0]))
        self.assertEqual(byting.binize(b[0]), '10110000')
        b = bytearray([0, 0, 0, 0, 0, 0])
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = byting.packifyInto(b, fmt=fmt, fields=fields)
        self.assertEqual(size, 3)
        self.assertEqual(b, bytearray([165, 224, 65, 0, 0, 0]))
        b = bytearray([0, 0, 0, 0, 0, 0])
        size = byting.packifyInto(b, fmt=fmt, fields=fields, offset=1)
        self.assertEqual(size, 3)
        self.assertEqual(b, bytearray([0, 165, 224, 65, 0, 0]))
        b = bytearray()
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = byting.packifyInto(b, fmt=fmt, fields=fields)
        self.assertEqual(size, 3)
        self.assertEqual(b, bytearray([165, 224, 65]))
        fmt = '3 2 1 1'
        fields = [6, 2, True, False]
        b = bytearray([0, 0, 0, 0, 0, 0])
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=1, reverse=True)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([212, 0, 0, 0, 0, 0]))
        self.assertEqual(byting.binize(b[0]), '11010100')
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=1, offset=2, reverse=True)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([212, 0, 212, 0, 0, 0]))
        self.assertEqual(byting.binize(b[2]), '11010100')
        b[0] = 0
        self.assertEqual(b, bytearray([0, 0, 212, 0, 0, 0]))
        size = byting.packifyInto(b, fmt=fmt, fields=fields, reverse=True)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([212, 0, 212, 0, 0, 0]))
        self.assertEqual(byting.binize(b[0]), '11010100')
        b = bytearray([0, 0, 0, 0, 0, 0])
        fmt = ''
        fields = []
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=0, reverse=True)
        self.assertEqual(size, 0)
        self.assertEqual(b, bytearray([0, 0, 0, 0, 0, 0]))
        size = byting.packifyInto(b, fmt=fmt, fields=fields, reverse=True)
        self.assertEqual(size, 0)
        self.assertEqual(b, bytearray([0, 0, 0, 0, 0, 0]))
        fmt = '3 1'
        fields = [5, True]
        size = byting.packifyInto(b, fmt=fmt, fields=fields, size=1, reverse=True)
        self.assertEqual(size, 1)
        self.assertEqual(b, bytearray([176, 0, 0, 0, 0, 0]))
        self.assertEqual(byting.binize(b[0]), '10110000')
        b = bytearray([0, 0, 0, 0, 0, 0])
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = byting.packifyInto(b, fmt=fmt, fields=fields, reverse=True)
        self.assertEqual(size, 3)
        self.assertEqual(b, bytearray([65, 224, 165, 0, 0, 0]))
        b = bytearray([0, 0, 0, 0, 0, 0])
        size = byting.packifyInto(b, fmt=fmt, fields=fields, offset=1, reverse=True)
        self.assertEqual(size, 3)
        self.assertEqual(b, bytearray([0, 65, 224, 165, 0, 0]))
        b = bytearray()
        fmt = '8 6 7 3'
        fields = [165, 56, 8, 1]
        size = byting.packifyInto(b, fmt=fmt, fields=fields, reverse=True)
        self.assertEqual(size, 3)
        self.assertEqual(b, bytearray([65, 224, 165]))

    def testSignExtend(self):
        """
        Test the signExtend function
        """
        console.terse('{0}\n'.format(self.testSignExtend.__doc__))
        a = 245
        self.assertEqual(a, 245)
        b = bytearray([245])
        y, x = byting.unpackify(fmt='3 5', b=b)
        self.assertEqual(x, 21)
        z = byting.signExtend(x, n=5)
        self.assertEqual(z, -11)
        a = 11
        self.assertEqual(a, 11)
        b = bytearray([11])
        y, x = byting.unpackify(fmt='3 5', b=b)
        self.assertEqual(x, 11)
        z = byting.signExtend(x, n=5)
        self.assertEqual(z, 11)
        a = 240
        self.assertEqual(a, 240)
        b = bytearray([240])
        y, x = byting.unpackify(fmt='3 5', b=b)
        self.assertEqual(x, 16)
        z = byting.signExtend(x, n=5)
        self.assertEqual(z, -16)
        a = 15
        self.assertEqual(a, 15)
        b = bytearray([15])
        y, x = byting.unpackify(fmt='3 5', b=b)
        self.assertEqual(x, 15)
        z = byting.signExtend(x, n=5)
        self.assertEqual(z, 15)
        a = 0
        self.assertEqual(a, 0)
        b = bytearray([0])
        y, x = byting.unpackify(fmt='3 5', b=b)
        self.assertEqual(x, 0)
        z = byting.signExtend(x, n=5)
        self.assertEqual(z, 0)


def runOne(test):
    """
    Unittest Runner
    """
    test = BasicTestCase(test)
    suite = unittest.TestSuite([test])
    unittest.TextTestRunner(verbosity=2).run(suite)


def runSome():
    """ Unittest runner """
    tests = []
    names = [
     'testBinizeUnbinize',
     'testBytifyUnbytify',
     'testPackifyUnpackify',
     'testPackifyInto',
     'testSignExtend']
    tests.extend(map(BasicTestCase, names))
    suite = unittest.TestSuite(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)


def runAll():
    """ Unittest runner """
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(BasicTestCase))
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    if __package__ is None:
        runSome()