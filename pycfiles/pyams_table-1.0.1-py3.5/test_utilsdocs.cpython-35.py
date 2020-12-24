# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/tests/test_utilsdocs.py
# Compiled at: 2019-12-05 08:40:48
# Size of source mod 2**32: 1825 bytes
"""
Generic test case for pyams_table doctests
"""
__docformat__ = 'restructuredtext'
import doctest, os, unittest
from pyams_table.tests import get_package_dir
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def doc_suite(test_dir, setUp=None, tearDown=None, globs=None):
    """Returns a test suite, based on doctests found in /doctests"""
    suite = []
    if globs is None:
        globs = globals()
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    package_dir = get_package_dir(test_dir)
    doctest_dir = os.path.join(package_dir, 'doctests')
    docs = [os.path.join(doctest_dir, doc) for doc in os.listdir(doctest_dir) if doc.endswith('.txt') or doc.endswith('.rst')]
    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, globs=globs, setUp=setUp, tearDown=tearDown, module_relative=False))

    return unittest.TestSuite(suite)


def test_suite():
    """Returns the test suite"""
    return doc_suite(CURRENT_DIR)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')