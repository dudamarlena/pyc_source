# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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