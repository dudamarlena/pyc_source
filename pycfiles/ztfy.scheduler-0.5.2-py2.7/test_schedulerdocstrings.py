# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/tests/test_schedulerdocstrings.py
# Compiled at: 2012-10-22 06:18:07
"""
Generic Test case for ztfy.scheduler doc strings
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os
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
    docs = [ doc for doc in os.listdir(package_dir) if doc.endswith('.py')
           ]
    docs = [ doc for doc in docs if not doc.startswith('__') ]
    for test in docs:
        fd = open(os.path.join(package_dir, test))
        content = fd.read()
        fd.close()
        if '>>> ' not in content:
            continue
        test = test.replace('.py', '')
        location = 'ztfy.scheduler.%s' % test
        suite.append(doctest.DocTestSuite(location, optionflags=flags, globs=globs))

    return unittest.TestSuite(suite)


def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')