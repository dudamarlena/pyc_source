# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/tests/test_workflowdocs.py
# Compiled at: 2012-06-26 16:56:38
"""
Generic Test case for ztfy.workflow doctest
"""
__docformat__ = 'restructuredtext'
import unittest, doctest, sys, os
current_dir = os.path.dirname(__file__)

def doc_suite(test_dir, setUp=None, tearDown=None, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)
    doctest_dir = os.path.join(package_dir, 'doctests')
    docs = [ os.path.join(doctest_dir, doc) for doc in os.listdir(doctest_dir) if doc.endswith('.txt')
           ]
    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, globs=globs, setUp=setUp, tearDown=tearDown, module_relative=False))

    return unittest.TestSuite(suite)


def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')