# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/tests/testSetup.py
# Compiled at: 2009-03-31 04:47:32
from Products.CMFCore.utils import getToolByName
from quintagroup.pingtool.config import PROJECTNAME
from base import *
from config import INSTALLED_TYPES, CONFIGLET

class TestSetup(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.qi = getToolByName(self.portal, 'portal_quickinstaller', None)
        self.ttool = getToolByName(self.portal, 'portal_types', None)
        self.ptool = getToolByName(self.portal, 'portal_properties', None)
        self.ctool = getToolByName(self.portal, 'portal_controlpanel', None)
        return

    def test_installed_uninstalled_products(self):
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), False, '%s is already installed' % PROJECTNAME)
        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)

    def test_tool_install_uninstall(self):
        tname = 'portal_pingtool'
        t = getToolByName(self.portal, tname, None)
        self.assertNotEqual(t, False, 'Tool %s not found after installation' % tname)
        self.failUnless(t, t)
        self.failUnless(isinstance(t, PingTool.PingTool), t.__class__)
        self.failUnlessEqual(t.meta_type, 'PingTool')
        self.failUnlessEqual(t.getId(), tname)
        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)
        t = getToolByName(self.portal, tname, None)
        self.assertNotEqual(t, True, 'Tool %s found after uninstallation' % tname)
        return

    def test_install_uninstall_types(self):
        ttool = self.ttool
        tids = ttool.objectIds()
        for id in INSTALLED_TYPES:
            self.assertNotEqual(id in tids, False, 'Type %s not found after installation' % id)
            tinfo = ttool[id]
            self.failUnless(tinfo.product == PROJECTNAME, tinfo.product)

        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)
        tids = ttool.objectIds()
        for id in INSTALLED_TYPES:
            self.assertNotEqual(id in tids, True, 'Type %s found after uninstallation' % id)

    def test_actions_install_uninstall(self):
        action = 'ping'
        ttool = self.ttool
        portal_action = getToolByName(self.portal, 'portal_actions')
        object_buttons = portal_action.object_buttons
        pt_actions_ids = [ a.id for a in object_buttons.listActions() ]
        self.assertNotEqual(action in pt_actions_ids, False, 'Action for %s not found after installation' % action)
        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)
        pt_actions_ids = [ a.id for a in object_buttons.listActions() ]
        self.assertNotEqual(action in pt_actions_ids, True, 'Action for %s found after uninstallation' % action)

    def test_configlet_install_uninstall(self):
        configTool = self.ctool
        self.assert_(CONFIGLET in [ a.getId() for a in configTool.listActions() ], 'Configlet not found')
        self.qi.uninstallProducts([PROJECTNAME])
        self.assertNotEqual(self.qi.isProductInstalled(PROJECTNAME), True, '%s is already installed' % PROJECTNAME)
        self.assert_(CONFIGLET not in [ a.getId() for a in configTool.listActions() ], 'Configlet found after uninstallation')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSetup))
    return suite