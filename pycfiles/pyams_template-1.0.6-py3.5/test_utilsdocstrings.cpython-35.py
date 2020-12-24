# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_template/tests/test_utilsdocstrings.py
# Compiled at: 2020-02-18 19:35:21
# Size of source mod 2**32: 1867 bytes
"""
Generic test case for pyams_template docstrings
"""
__docformat__ = 'restructuredtext'
import doctest, os, unittest
from pyams_template.tests import get_package_dir
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def doc_suite(test_dir, globs=None):
    """Returns a test suite, based on doc tests strings found in /*.py"""
    suite = []
    if globs is None:
        globs = globals()
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    package_dir = get_package_dir(test_dir)
    docs = [doc for doc in os.listdir(package_dir) if doc.endswith('.py')]
    docs = [doc for doc in docs if not doc.startswith('__')]
    for test in docs:
        fd = open(os.path.join(package_dir, test))
        content = fd.read()
        fd.close()
        if '>>> ' not in content:
            pass
        else:
            test = test.replace('.py', '')
            location = 'pyams_template.%s' % test
            suite.append(doctest.DocTestSuite(location, optionflags=flags, globs=globs))

    return unittest.TestSuite(suite)


def test_suite():
    """returns the test suite"""
    return doc_suite(CURRENT_DIR)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')