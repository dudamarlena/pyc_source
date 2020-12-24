# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\QuillsEnabledRemoteBlogging\tests\test_doctests.py
# Compiled at: 2008-04-09 20:30:20
import unittest
from doctest import DocTestSuite
import zope.component.testing

def setUp(test):
    pass


suites = (
 DocTestSuite('quills.app.remoteblogging.uidmanager', setUp=zope.component.testing.setUp, tearDown=zope.component.testing.tearDown), DocTestSuite('quills.app.remoteblogging.usermanager', setUp=zope.component.testing.setUp, tearDown=zope.component.testing.tearDown))

def test_suite():
    return unittest.TestSuite(suites)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')