# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/releaser/tests/test_releaserdocstrings.py
# Compiled at: 2008-04-29 08:14:25
"""
Generic Test case for iw.releaser doc strings
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os
from iw.releaser import testing
from zope.testing import doctest
current_dir = os.path.abspath(os.path.dirname(__file__))

def doc_suite(test_dir, globs=None):
    """Returns a test suite, based on doc tests strings found in /*.py"""
    suite = []
    if globs is None:
        globs = globals()
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)
    docs = [ doc for doc in os.listdir(package_dir) if doc.endswith('.py') ]
    docs = [ doc for doc in docs if not doc.startswith('__') ]
    docs = [ doc for doc in docs if doc not in ['config.py'] ]
    for test in docs:
        fd = open(os.path.join(package_dir, test))
        content = fd.read()
        fd.close()
        if '>>> ' not in content:
            continue
        test = test.replace('.py', '')
        suite.append(doctest.DocTestSuite('iw.releaser.%s' % test, optionflags=flags, globs=globs, setUp=testing.releaserSetUp, tearDown=testing.releaserTearDown))

    return unittest.TestSuite(suite)


def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')