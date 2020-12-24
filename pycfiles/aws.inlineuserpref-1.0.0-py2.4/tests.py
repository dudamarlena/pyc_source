# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/aws/inlineuserpref/tests.py
# Compiled at: 2009-12-16 04:54:04
"""All tests of aws.inlineuserpref"""
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from zope.component import getMultiAdapter
from plone.app.controlpanel.site import ISiteSchema
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
from aws.inlineuserpref.controlpanel import IInlineEditOption
from archetypes.kss.interfaces import IInlineEditingEnabled

@onsetup
def setupPackage():
    fiveconfigure.debug_mode = True
    import aws.inlineuserpref
    zcml.load_config('configure.zcml', aws.inlineuserpref)
    zcml.load_config('overrides.zcml', aws.inlineuserpref)
    fiveconfigure.debug_mode = False
    ZopeTestCase.installPackage('aws.inlineuserpref', quiet=True)


setupPackage()
PloneTestCase.setupPloneSite(products=['aws.inlineuserpref'])

class InlineUserPrefTestCase(PloneTestCase.PloneTestCase):
    """Main testcase effective class
    """
    __module__ = __name__

    def test_install(self):
        """Checking essential GS installed stuffs
        """
        tool = self.portal.portal_memberdata
        self.failUnlessEqual(tool.getProperty('enable_inline_editing'), True, "Missing 'enable_inline_editing' property")
        tool = self.portal.portal_actionicons
        ai = tool.getActionInfo('controlpanel', 'inline_edit')
        self.failUnlessEqual(len(ai), 3, 'We have no action icon')
        tool = self.portal.portal_controlpanel
        configlets = tool.enumConfiglets(group='Member')
        cids = [ c['id'] for c in configlets ]
        self.failUnless('inline_edit' in cids, 'Our configlet is not installed')
        from plone.browserlayer import utils as bl_utils
        from aws.inlineuserpref.interfaces import IAWSInlineUserPrefLayer
        self.failUnless(IAWSInlineUserPrefLayer in bl_utils.registered_layers(), 'Our layer is not registered')

    def test_defaultsetup(self):
        """Default behaviour
        """
        site_schema = ISiteSchema(self.portal)
        self.failUnlessEqual(site_schema.enable_inline_editing, False, 'Globale inline editing should be disabled')
        self._loginAsUser1()
        user_option = IInlineEditOption(self.portal)
        self.failUnlessEqual(user_option.enable_inline_editing, True, 'Personal inline editing should be enabled by default')
        view = getMultiAdapter((self.portal['front-page'], self.portal.REQUEST), IInlineEditingEnabled)

    def test_enabled_everywhere(self):
        """Inline editing is enabled on site and for the user
        """
        self._loginAsUser1()
        site_schema = ISiteSchema(self.portal)
        site_schema.enable_inline_editing = True
        user_option = IInlineEditOption(self.portal)
        user_option.enable_inline_editing = True
        view = getMultiAdapter((self.portal['front-page'], self.portal.REQUEST), IInlineEditingEnabled)
        self.failUnless(view(), 'Resulting inline editing should be enabled to user')

    def test_site_enabled_user_disabled(self):
        """Inline editing is enabled only for site and not to the user
        """
        self._loginAsUser1()
        site_schema = ISiteSchema(self.portal)
        site_schema.enable_inline_editing = True
        user_option = IInlineEditOption(self.portal)
        user_option.enable_inline_editing = False
        view = getMultiAdapter((self.portal['front-page'], self.portal.REQUEST), IInlineEditingEnabled)
        self.failIf(view(), 'Resulting inline editing should be disabled to user')

    def _loginAsUser1(self):
        """Self speaking ;)
        """
        aclusers = self.portal.acl_users
        user1 = aclusers.getUserById('user1')
        if user1 is None:
            aclusers._doAddUser('user1', 'secret', ['Member'], [], [])
            user1 = aclusers.getUserById('user1')
        if not hasattr(user1, 'aq_base'):
            user1 = user1.__of__(aclusers)
        newSecurityManager(None, user1)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(InlineUserPrefTestCase))
    return suite