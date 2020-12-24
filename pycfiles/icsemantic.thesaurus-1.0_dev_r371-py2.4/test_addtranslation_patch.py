# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/tests/test_addtranslation_patch.py
# Compiled at: 2008-10-06 10:31:07
"""Tests
"""
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import PloneSite
from icsemantic.thesaurus.config import *
import base

class FunctionalTestConfiglets(base.icSemanticFunctionalTestCase):
    """
    """
    __module__ = __name__


def test_suite():
    return unittest.TestSuite([ztc.FunctionalDocFileSuite('test_addtranslation_patch.txt', package=PACKAGENAME + '.tests', test_class=FunctionalTestConfiglets)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')