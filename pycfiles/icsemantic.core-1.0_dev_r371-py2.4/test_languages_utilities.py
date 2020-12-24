# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/core/tests/test_languages_utilities.py
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
import base

class UnitTests(base.icSemanticTestCase):
    """
    """
    __module__ = __name__


class FunctionalTests(base.icSemanticFunctionalTestCase):
    """
    """
    __module__ = __name__


def test_suite():
    return unittest.TestSuite([ztc.ZopeDocTestSuite(module=PACKAGENAME + '.memberdata.languages', test_class=UnitTests), ztc.FunctionalDocFileSuite('test_languages_utilities.txt', package=PACKAGENAME + '.tests', test_class=FunctionalTests)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')