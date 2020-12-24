# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/eCards/tests/test_permissions.py
# Compiled at: 2008-11-11 20:26:20
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.eCards.tests import base
from Products.eCards.config import SendECard

class TestProductPermissions(base.eCardTestCase):
    """ Ensure that our eCard product classes and objects
        fullfill their contractual interfaces
    """
    __module__ = __name__

    def afterSetUp(self):
        self.setupCollection()
        self.setupContainedECard()
        self.ecard = self.folder.collection.ecard
        self.view = self.ecard.restrictedTraverse('ecardpopup_browserview')
        self.membership = self.portal.portal_membership

    def testCustomECardPermissionConfigured(self):
        """We setup a permission for the sending of eCards that can easily 
           be overridden in cases where this is wanted as a priveleged feature.
        """
        self.failUnless('eCards: Send eCard' in [ r['name'] for r in self.portal.permissionsOfRole('Manager') if r['selected'] ])
        self.failUnless('eCards: Send eCard' in [ r['name'] for r in self.portal.permissionsOfRole('Anonymous') if r['selected'] ])

    def testAnonHasAccessToPopupView(self):
        """Our view is protected by the eCards.SendECard permission
           We ensure that anonymous can access that view by default
        """
        self.logout()
        self.failUnless(self.portal.portal_membership.isAnonymousUser())
        self.failUnless(self.membership.checkPermission(SendECard, self.ecard))

    def testViewProtectedUponRoleModification(self):
        """Our view is protected by the eCards.SendECard permission, which
           by default should be allowable by all.
           
           However we want people to be able make this "anonymous"
           protected activity.  The following test demonstrates that.
        """
        self.portal.manage_permission(SendECard, ('Manager', ), acquire=0)
        self.failIf('eCards: Send eCard' in [ r['name'] for r in self.portal.permissionsOfRole('Anonymous') if r['selected'] ])
        self.logout()
        self.failUnless(self.portal.portal_membership.isAnonymousUser())
        self.failIf(self.membership.checkPermission(SendECard, self.ecard))


if __name__ == '__main__':
    framework()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductPermissions))
    return suite