# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/cache/tests/test_cachedocs.py
# Compiled at: 2007-12-05 09:41:22
"""
Generic Test case for 'cache' doctest
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os
from zope.testing import doctest
from iw.cache.testing import cacheSetUp
from iw.cache.testing import cacheTearDown
current_dir = os.path.dirname(__file__)

def doc_suite(test_dir, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)
    doctest_dir = os.path.join(package_dir, 'doctests')
    docs = [ os.path.join(doctest_dir, doc) for doc in os.listdir(doctest_dir) if doc.endswith('.txt') ]
    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, globs=globs, module_relative=False, setUp=cacheSetUp, tearDown=cacheTearDown))

    return unittest.TestSuite(suite)


def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')