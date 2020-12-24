# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/tests/test_bugs.py
# Compiled at: 2008-10-06 10:31:08
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import PloneSite
from icsemantic.core.config import *
import base, utils

def test_suite():
    suite = unittest.TestSuite()
    filenames = utils.list_functionaltests('bugs')
    for docfile in filenames:
        suite.addTest(ztc.FunctionalDocFileSuite(docfile, package='icsemantic.core.tests', test_class=base.icSemanticFunctionalTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')