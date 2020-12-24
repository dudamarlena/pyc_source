# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/tests/test_property_langview_language.py
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

class TestPropertyLangviewLanguage(base.icSemanticTestCase):
    __module__ = __name__

    def testInstalled(self):
        """
        >>> memberdata = self.portal.portal_memberdata
        >>> [property for property in memberdata.propertyMap() if property['id'] == 'icsemantic.preferred_languages']
        [{'type':...'lines', 'id': 'icsemantic.preferred_languages'}]
        """
        pass

    def testAssignValue(self):
        """
        >>> portal = self.portal
        >>> memberdata = self.portal.portal_memberdata
        >>> member1 = portal.portal_registration.addMember('test1', 'test1')
        >>> member1
        <MemberData at /plone/portal_memberdata/test1 used for /plone/acl_users>
    
        >>> member1.setMemberProperties({'icsemantic.preferred_languages': ('en', 'es', 'it')})
        >>> member1.getProperty('icsemantic.preferred_languages')
        ('en', 'es', 'it')
        """
        pass

    def testUnInstalled(self):
        """
        >>> from icsemantic.langfallback.config import *
        >>> qi = self.portal.portal_quickinstaller
        >>> qi.uninstallProducts((PACKAGENAME,))
        >>> memberdata = self.portal.portal_memberdata
        >>> [property for property in memberdata.propertyMap() if property['id'] == 'icsemantic.preferred_languages']
        []
        """
        pass


def test_suite():
    return unittest.TestSuite([ztc.ZopeDocTestSuite(test_class=TestPropertyLangviewLanguage), ztc.FunctionalDocFileSuite('test_property_langview_language.txt', package=PACKAGENAME + '.tests', test_class=base.icSemanticFunctionalTestCase)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')