# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aid/test/test_osetting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 2552 bytes
"""
Unit Test Template
"""
from __future__ import absolute_import, division, print_function
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os
from ioflo.aid.sixing import *
from ioflo.test import testing
from ioflo.aid.consoling import getConsole
console = getConsole()
from ioflo.aid import osetting

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

    def testOset(self):
        """
        Test the oset
        """
        console.terse('{0}\n'.format(self.testOset.__doc__))
        s = osetting.oset('abracadaba')
        l = ['a', 'b', 'r', 'c', 'd']
        x = osetting.oset(l)
        self.assertEqual(s, x)
        for i, e in enumerate(s):
            self.assertEqual(l[i], e)

        t = osetting.oset('simsalabim')
        y = osetting.oset(['s', 'i', 'm', 'a', 'l', 'b'])
        self.assertEqual(t, y)
        self.assertEqual(s | t, osetting.oset('abrcdsiml'))
        self.assertEqual(s & t, osetting.oset('ab'))
        self.assertEqual(s - t, osetting.oset('rcd'))
        self.assertFalse(s == t)
        self.assertTrue(s == s)
        u = osetting.oset(s)
        self.assertTrue(s == u)
        self.assertFalse(s is u)


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
     'testOset']
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