# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\QuillsRemoteBlogging\tests\test_doctests.py
# Compiled at: 2008-06-04 06:25:04
import unittest
from doctest import DocTestSuite
import zope.component.testing

def setUp(test):
    pass


suites = (
 DocTestSuite('Products.QuillsRemoteBlogging.uidmanager', setUp=zope.component.testing.setUp, tearDown=zope.component.testing.tearDown), DocTestSuite('Products.QuillsRemoteBlogging.usermanager', setUp=zope.component.testing.setUp, tearDown=zope.component.testing.tearDown))

def test_suite():
    return unittest.TestSuite(suites)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')