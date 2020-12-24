# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/brainfreeze/test/test_docs.py
# Compiled at: 2008-07-31 12:30:03
__doc__ = 'Test suite for python examples embedded in the documentation'
import os, doctest

def test_suite():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    brainfreeze_dir = os.path.dirname(test_dir)
    doc_dir = os.path.join(brainfreeze_dir, 'doc', 'src')
    doc_files = []
    for (root, dirs, files) in os.walk(doc_dir):
        for name in files:
            if name.endswith('.txt'):
                path = os.path.join(root, name)
                doc_files.append(path)

    kw = dict(module_relative=False)
    return doctest.DocFileSuite(*doc_files, **kw)


if __name__ == '__main__':
    import sys, unittest
    if sys.version_info[:2] < (2, 4):
        print 'Python 2.4 or later required for tests (%d.%d detected).' % sys.version_info[:2]
        sys.exit(-1)
    unittest.TextTestRunner().run(test_suite())