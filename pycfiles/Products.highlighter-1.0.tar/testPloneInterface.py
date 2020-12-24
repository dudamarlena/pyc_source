# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/tests/testPloneInterface.py
# Compiled at: 2008-05-20 04:51:55
__doc__ = '\n\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
PloneTestCase.setupPloneSite()
from AccessControl.Permissions import access_contents_information, view, add_documents_images_and_files, change_images_and_files, view_management_screens
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager, getSecurityManager
from AccessControl import Unauthorized
from AccessControl.User import UnrestrictedUser
import urllib
app = ZopeTestCase.app()
ZopeTestCase.utils.setupSiteErrorLog(app)
ZopeTestCase.close(app)
(host, port) = ZopeTestCase.utils.startZServer(4)
base = 'http://%s:%d/%s' % (host, port, ZopeTestCase.folder_name)
ZopeTestCase.installProduct('GroupUserFolder')
try:
    import Log
    Log.LOG_LEVEL = Log.LOG_DEBUG
    Log.LOG_PROCESSOR = {Log.LOG_NONE: Log.logFile, Log.LOG_CRITICAL: Log.logFile, Log.LOG_ERROR: Log.logFile, Log.LOG_WARNING: Log.logFile, Log.LOG_NOTICE: Log.logFile, Log.LOG_DEBUG: Log.logFile}
    from Log import *
    Log(LOG_NOTICE, 'Starting %s at %d debug level' % (os.path.dirname(__file__), LOG_LEVEL))
except:
    print 'Log module not available'
    LOG_DEBUG = None
    LOG_NOTICE = None
    LOG_WARNING = None
    LOG_ERROR = None
    LOG_CRITICAL = None

    def Log(*args, **kw):
        pass


    raise

class ManagementOpener(urllib.FancyURLopener):
    __module__ = __name__

    def prompt_user_passwd(self, host, realm):
        return ('manager', 'secret')


class UnauthorizedOpener(urllib.FancyURLopener):
    __module__ = __name__

    def prompt_user_passwd(self, host, realm):
        raise Unauthorized, 'The URLopener was asked for authentication'


class TestPloneInterface(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginPortalOwner()
        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct('GroupUserFolder')
        self.mt = self.portal.portal_membership
        self.gt = self.portal.portal_groups
        self.acl_users = self.portal.acl_users

    def testUserCreation(self):
        """
        test user creation with plone
        """
        self.mt.addMember('member1', 'secret', ['Member'], None)
        self.failUnless('member1' in self.acl_users.getUserNames())
        self.failUnless('Member' in self.acl_users.getUser('member1').getRoles())
        return

    def testGroupCreation(self):
        """
        test group creation with plone
        """
        self.gt.addGroup('group1', roles=['Member'])
        self.failUnless('group_group1' in self.acl_users.getGroupNames())
        self.failUnless('Member' in self.acl_users.getGroup('group_group1').getRoles())
        self.portal._addRole('SampleRole')
        self.gt.addGroup('group2', roles=['SampleRole'])
        self.failUnless('SampleRole' in self.acl_users.getGroup('group_group2').getRoles())
        self.failUnless('Member' not in self.acl_users.getGroup('group_group2').getRoles())

    def testUserToGroup(self):
        """
        test user and group interaction with Plone API
        """
        self.portal._addRole('SampleRole')
        self.gt.addGroup('group2', roles=['SampleRole'])
        self.mt.addMember('member1', 'secret', ['Member'], None)
        group = self.gt.getGroupById('group2')
        group.addMember('member1')
        Log(LOG_DEBUG, group.getGroupMemberIds())
        self.failUnless('member1' in group.getGroupMemberIds())
        return

    def testUserToGroupRoles(self):
        self.portal._addRole('SampleRole')
        self.gt.addGroup('group2', roles=['SampleRole'])
        self.mt.addMember('member1', 'secret', ['Member'], None)
        group = self.gt.getGroupById('group2')
        group.addMember('member1')
        self.failUnless('SampleRole' in self.acl_users.getUser('member1').getRoles())
        self.failUnless('Member' in self.acl_users.getUser('member1').getRoles())
        self.failUnless('SampleRole' not in self.acl_users.getUser('member1').getUserRoles())
        return

    def testUserToGroupRolesBug(self):
        self.portal._addRole('SampleRole')
        self.gt.addGroup('group2', roles=['SampleRole'])
        self.mt.addMember('member1', 'secret', ['Member'], None)
        group = self.gt.getGroupById('group2')
        group.addMember('member1')
        group.addMember('member1')
        self.failIf('SampleRole' in self.acl_users.getUser('member1').getUserRoles())
        return

    def testUserToGroupRemoving(self):
        self.portal._addRole('SampleRole')
        self.gt.addGroup('group2', roles=['SampleRole'])
        self.mt.addMember('member1', 'secret', ['Member'], None)
        group = self.gt.getGroupById('group2')
        group.addMember('member1')
        group.removeMember('member1')
        self.failUnless('member1' not in group.getGroupMembers())
        self.failUnless('SampleRole' not in self.acl_users.getUser('member1').getRoles())
        self.failUnless('Member' in self.acl_users.getUser('member1').getRoles())
        return


if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        return suite