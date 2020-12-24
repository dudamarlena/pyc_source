# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/test/testTemplate.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 1722 bytes
"""
Unit Test Template
"""
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import os
from ioflo.test import testing
from ioflo.aid.consoling import getConsole
console = getConsole()

def setUpModule():
    console.reinit(verbosity=(console.Wordage.concise))


def tearDownModule():
    pass


class BasicTestCase(testing.FrameIofloTestCase):
    __doc__ = '\n    Example TestCase\n    '

    def setUp(self):
        super(BasicTestCase, self).setUp()

    def tearDown(self):
        super(BasicTestCase, self).tearDown()

    def testBasic(self):
        """
        Example test
        """
        console.terse('{0}\n'.format(self.testBasic.__doc__))


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
     '']
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
        runAll()