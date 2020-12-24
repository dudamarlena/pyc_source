# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/tests/test_skins.py
# Compiled at: 2008-10-06 10:31:06
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import PloneSite
from icsemantic.langfallback.config import *
import base

class TestSkins(base.icSemanticTestCase):
    """
    """
    __module__ = __name__

    def testRegistered(self):
        """
            >>> portal = self.portal
            >>> skinstool = portal.portal_skins
            >>> skinstool
            <SkinsTool at /plone/portal_skins>
            >>> 'icsemantic.langfallback' in skinstool.getSkinPath('Plone Default')
            True

        """
        pass

    def testLayersOrder(self):
        """
            >>> portal = self.portal
            >>> skinstool = portal.portal_skins
            >>> path = skinstool.getSkinPath('Plone Default')
            >>> 'icsemantic.langfallback' in path
            True
            >>> 'LinguaPlone' in path
            True
            >>> path.index('icsemantic.langfallback') < path.index('LinguaPlone')
            True

        """
        pass


def test_suite():
    return unittest.TestSuite([ztc.ZopeDocTestSuite(test_class=TestSkins), ztc.FunctionalDocFileSuite('test_skins.txt', package=PACKAGENAME + '.tests', test_class=base.icSemanticFunctionalTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')