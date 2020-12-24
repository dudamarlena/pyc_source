# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grokimdb/ftests.py
# Compiled at: 2008-01-27 19:50:14
import unittest, os.path, grok
from zope.testing import doctest
from zope.app.testing.functional import HTTPCaller, getRootFolder, FunctionalTestSetup, sync, ZCMLLayer, FunctionalDocFileSuite
DOCTESTFILES = [
 'browser.txt']
ftesting_zcml = os.path.join(os.path.dirname(grok.__file__), 'ftesting.zcml')
GrokIMDBFunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'GrokIMDBFunctionalLayer')

def setUp(test):
    FunctionalTestSetup().setUp()


def tearDown(test):
    FunctionalTestSetup().tearDown()


def suiteFromFile(name):
    suite = unittest.TestSuite()
    test = FunctionalDocFileSuite(name, setUp=setUp, tearDown=tearDown, encoding='utf-8', globs=dict(http=HTTPCaller(), getRootFolder=getRootFolder, sync=sync), optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE + doctest.REPORT_NDIFF)
    test.layer = GrokIMDBFunctionalLayer
    suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in DOCTESTFILES:
        suite.addTest(suiteFromFile(name))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')