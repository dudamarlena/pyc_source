# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/tests/test_docs.py
# Compiled at: 2008-10-23 05:55:15
"""
Generic Test case for iw.fss doctests
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.publisher.browser import TestRequest
from Products.Five.testbrowser import Browser
from iw.fss import strategy
from iw.fss.conffile import ConfFile
from base import TestCase, STORAGE_PATH, BACKUP_PATH
current_dir = os.path.dirname(__file__)

def doc_suite(test_dir, setUp=None, tearDown=None, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()
    globs['test_dir'] = current_dir
    browser = Browser()
    browser.handleErrors = False
    globs['browser'] = browser
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE | doctest.REPORT_UDIFF
    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)
    docs = []
    for dir_ in ('doctests', ):
        doctest_dir = os.path.join(package_dir, dir_)
        docs.extend([ os.path.join(doctest_dir, doc) for doc in os.listdir(doctest_dir) if doc.endswith('.txt') ])

    for test in docs:
        suite.append(FunctionalDocFileSuite(test, optionflags=flags, globs=globs, setUp=setUp, tearDown=tearDown, test_class=TestCase, module_relative=False))

    return suite


def test_suite():
    """returns the test suite"""
    strategies = ('FlatStorageStrategy', 'DirectoryStorageStrategy', 'SiteStorageStrategy',
                  'SiteStorageStrategy2')

    def changeStrategy(self):
        strategy_klass = self.globs['strategy_klass'](STORAGE_PATH, BACKUP_PATH)
        ConfFile.getStorageStrategy = lambda x: strategy_klass

    suite = []
    for strategy_name in strategies:
        strategy_klass = getattr(strategy, strategy_name)
        suite.extend(doc_suite(current_dir, globs={'strategy_klass': strategy_klass}, setUp=changeStrategy))

    return unittest.TestSuite(suite)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')