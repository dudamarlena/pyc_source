# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/zope2/tests/test_docs.py
# Compiled at: 2008-07-24 14:48:01
import unittest
from zope.testing.doctest import DocFileSuite, REPORT_NDIFF, ELLIPSIS
options = REPORT_NDIFF | ELLIPSIS

def addPythonScript(c, name, source):
    c.manage_addProduct['PythonScripts'].manage_addPythonScript(name)
    getattr(c, name).write(source)


def setUp(test):
    from Testing.makerequest import makerequest
    from Zope2 import app
    a = makerequest(app())
    a.manage_addFolder('folder')
    test.globs['folder'] = a.folder
    test.globs['request'] = a.REQUEST
    test.globs['addPythonScript'] = addPythonScript


def test_suite():
    suite = unittest.TestSuite()
    try:
        import Zope2
    except ImportError:
        return suite

    suite.addTest(DocFileSuite('../readme.txt', optionflags=options, setUp=setUp))
    return suite


if __name__ == '__main__':
    unittest.main(default='test_suite')