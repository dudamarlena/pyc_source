# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/tests/test_README.py
# Compiled at: 2006-02-26 23:54:33
import unittest
from zope.testing.doctest import DocFileTest

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(DocFileTest('../README.txt'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')