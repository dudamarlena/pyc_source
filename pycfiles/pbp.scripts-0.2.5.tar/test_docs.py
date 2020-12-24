# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/MacDev/perso/atomisator.ziade.org/packages/pbp.scripts/pbp/scripts/tests/test_docs.py
# Compiled at: 2008-06-09 07:35:12
import unittest, doctest, os
test_dir = os.path.dirname(__file__)
package_dir = os.path.split(test_dir)[0]

def doc_suite(test_dir):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    globs = globals()
    flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    doctest_dir = os.path.join(package_dir, 'docs')
    docs = [ os.path.join(doctest_dir, doc) for doc in os.listdir(doctest_dir) if doc.endswith('.txt') ]
    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags, globs=globs, module_relative=False))

    return unittest.TestSuite(suite)


def test_suite():
    """Returns the test suite."""
    return doc_suite(test_dir)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')