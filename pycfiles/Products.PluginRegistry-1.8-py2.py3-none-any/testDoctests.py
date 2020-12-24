# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/pluggablecatalog/tests/testDoctests.py
# Compiled at: 2008-07-23 15:36:19
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import ZopeDocTestSuite
from Products.pluggablecatalog.tests import common
common.setupPloneSite()
from Products.PloneTestCase import PloneTestCase
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE

def test_suite():
    return unittest.TestSuite([ ZopeDocTestSuite(module, test_class=PloneTestCase.PloneTestCase, optionflags=optionflags) for module in ('Products.pluggablecatalog.tool', ) ])