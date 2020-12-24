# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/plonetheme/terrafirma/tests/test_setup.py
# Compiled at: 2008-05-03 14:33:00
import unittest
from plonetheme.terrafirma.tests.base import TerrafirmaTestCase
from Products.CMFCore.utils import getToolByName

class TestSetup(TerrafirmaTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')
        self.css = getToolByName(self.portal, 'portal_css')
        self.skins = getToolByName(self.portal, 'portal_skins')

    def test_theme_installed(self):
        layer = self.skins.getSkinPath('Terrafirma Theme')
        self.failUnless('plonetheme_terrafirma_styles' in layer)
        self.assertEquals('Terrafirma Theme', self.skins.getDefaultSkin())
        cssTitles = [ n.getTitle() for n in self.css.resources ]
        self.failUnless('Terrafirma CSS' in cssTitles)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite