# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Organization/tests/test_doctest.py
# Compiled at: 2011-06-07 12:12:00
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing, eventtesting
from Testing import ZopeTestCase as ztc
from Products.Organization.tests import base

def test_suite():
    return unittest.TestSuite([
     ztc.ZopeDocFileSuite('README.txt', package='Products.Organization', test_class=base.FunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')