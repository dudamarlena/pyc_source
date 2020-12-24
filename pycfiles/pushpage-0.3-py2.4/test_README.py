# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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