# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/test_docs.py
# Compiled at: 2007-02-15 03:32:44
import doctest, unittest, os
flags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
files = [ os.path.join('doc', filename) for filename in os.listdir('doc') if filename.endswith('.txt')
        ]

def cleanup():
    top = os.path.join(os.path.dirname(__file__), 'tests/www')
    for (root, dirs, files) in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

        for name in dirs:
            os.rmdir(os.path.join(root, name))


def test_suite():
    cleanup()
    suite = []
    for testfile in files:
        suite.append(doctest.DocFileTest(testfile, optionflags=flags))

    return unittest.TestSuite(suite)


if __name__ == '__main__':
    try:
        unittest.main(defaultTest='test_suite')
    finally:
        cleanup()