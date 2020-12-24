# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grokimdb/tests.py
# Compiled at: 2008-01-27 19:57:13
import unittest
from zope.testing import doctest, cleanup
import grokimdb
DOCTESTFILES = ['app.py', 'README.txt']

def setUpZope(test):
    pass


def cleanUpZope(test):
    cleanup.cleanUp()


def test_suite():
    suite = unittest.TestSuite()
    for name in DOCTESTFILES:
        suite.addTest(doctest.DocFileSuite(name, package=grokimdb, setUp=setUpZope, tearDown=cleanUpZope, encoding='utf8', optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')