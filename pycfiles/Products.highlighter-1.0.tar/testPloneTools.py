# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/tests/testPloneTools.py
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
import urllib, string
app = ZopeTestCase.app()
ZopeTestCase.utils.setupSiteErrorLog(app)
ZopeTestCase.close(app)
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.GroupUserFolder.interfaces import IUserFolder
from Products.GroupUserFolder import GroupUserFolder
from Products.GroupUserFolder import GroupsTool
from Products.GroupUserFolder import GroupDataTool
from Interface import Verify
ZopeTestCase.installProduct('GroupUserFolder')
import GRUFTestCase, testInterface
from Log import *

class GroupTestCase(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.membership = self.portal.portal_membership
        self.gruf = self.portal.acl_users
        self.groups = self.portal.portal_groups
        self.prefix = self.gruf.getGroupPrefix()
        self.groups.groupWorkspacesCreationFlag = 0
        self.groups.removeGroups(self.groups.listGroupIds())
        self.groups.addGroup('grp')
        self.groups.addGroup('g1')
        self.groups.addGroup('g2')
        self.groups.addGroup('g3')
        self.groups.addGroup('g4')
        self.membership.addMember('u1', 'secret', [], [])
        self.membership.addMember('u2', 'secret', [], [])
        self.membership.addMember('u3', 'secret', [], [])
        self.membership.addMember('u4', 'secret', [], [])
        self.membership.addMember('u5', 'secret', [], [])
        self.membership.addMember('u6', 'secret', [], [])
        self.membership.addMember('u7', 'secret', [], [])
        self.gruf.addMember('g1', 'u2')
        self.gruf.addMember('g1', 'u3')
        self.gruf.addMember('g1', 'u4')
        self.gruf.addMember('g2', 'u3')
        self.gruf.addMember('g2', 'u4')
        self.gruf.addMember('g2', 'u5')
        self.gruf.addMember('g3', 'u4')
        self.gruf.addMember('g3', 'u5')
        self.gruf.addMember('g3', 'u6')
        self.gruf.addMember('g4', 'u7')


class TestGroupsTool(GroupTestCase, testInterface.TestInterface):
    __module__ = __name__
    klasses = (GroupsTool.GroupsTool,)
    ignore_interfaces = (
     ActionProviderBase.__implements__,)

    def test_isGroup(self):
        g1 = self.groups.getGroupById('g1')
        g1.addMember('g2')
        ngroups = 0
        nusers = 0
        for u in g1.getGroupMembers():
            if self.groups.isGroup(u):
                ngroups += 1
            else:
                nusers += 1

        self.failUnlessEqual(ngroups, 1)
        self.failUnlessEqual(nusers, 3)

    def test_getGroupById(self):
        """Returns the portal_groupdata-ish object for a group corresponding
        to this id."""
        self.portal.portal_groups.addGroup('mygroup')
        g = self.portal.portal_groups.getGroupById('mygroup')
        self.failUnless(g, 'Emtpy or invalid group')

    def test_getGroupsByUserId(self):
        """Returns a list of the groups the user corresponding to 'userid' belongs to."""
        grps = self.groups.getGroupsByUserId('u3')
        ids = map(lambda x: x.getGroupName(), grps)
        ids.sort()
        self.failUnless(ids == ['g1', 'g2'], "Invalid groups: '%s'" % (ids,))

    def test_listGroups(self):
        """Returns a list of the available portal_groupdata-ish objects."""
        grps = self.groups.listGroups()
        ids = map(lambda x: x.getGroupName(), grps)
        self.failUnless(ids == ['g1', 'g2', 'g3', 'g4', 'grp'], "Invalid groups list: '%s'" % (ids,))

    def test_listGroupIds(self):
        """Returns a list of the available groups' ids."""
        ids = self.groups.listGroupIds()
        ids.sort()
        self.failUnless(ids == ['g1', 'g2', 'g3', 'g4', 'grp'], "Invalid groups list: '%s'" % (ids,))

    def test_listGroupNames(self):
        """Returns a list of the available groups' ids."""
        ids = self.groups.listGroupNames()
        ids.sort()
        self.failUnless(ids == ['g1', 'g2', 'g3', 'g4', 'grp'], "Invalid groups list: '%s'" % (ids,))

    def test_searchForGroups(self):
        """Return a list of groups meeting certain conditions. """
        pass

    def test_addGroup(self):
        """Create a group with the supplied id, roles, and domains.

        Underlying user folder must support adding users via the usual Zope API.
        Passwords for groups seem to be currently irrelevant in GRUF."""
        self.groups.addGroup('grptest1')
        self.failUnless('grptest1' in self.groups.listGroupIds())
        self.failUnlessRaises(ValueError, self.groups.addGroup, 'grptest1')
        self.groups.addGroup('grptest2', ['Reviewer'], ['grptest1'], description='Sample group')
        g = self.groups.getGroupById('grptest2')
        g1 = self.groups.getGroupById('grptest1')
        self.failUnlessEqual(g.getProperty('description'), 'Sample group')
        self.failUnless('grptest2' in g1.getGroupMemberIds(), g1.getGroupMemberIds())
        self.failUnless(self.gruf.getGroupByName('grptest2').has_role('Reviewer'))

    def test_editGroup(self):
        """Edit the given group with the supplied password, roles, and domains.

        Underlying user folder must support editing users via the usual Zope API.
        Passwords for groups seem to be currently irrelevant in GRUF."""
        self.groups.addGroup('grptest1')
        self.groups.addGroup('grptest2')
        self.groups.editGroup('grptest2', ['Reviewer'], ['grptest1'], description='Sample group')
        g = self.groups.getGroupById('grptest2')
        g1 = self.groups.getGroupById('grptest1')
        self.failUnlessEqual(g.getProperty('description'), 'Sample group')
        self.failUnless('group_grptest2' in g1.getGroup().getMemberIds(), g1.getGroup().getMemberIds())
        self.failUnless('grptest2' in g1.getGroupMemberIds(), g1.getGroupMemberIds())
        self.failUnless(self.gruf.getGroupByName('grptest2').has_role('Reviewer'))
        self.failUnlessRaises(ValueError, self.groups.editGroup, 'grptest_toto')

    def test_removeGroups(self):
        """Remove the group in the provided list (if possible).

        Will by default remove this group's GroupWorkspace if it exists. You may
        turn this off by specifying keep_workspaces=true.
        Underlying user folder must support removing users via the usual Zope API."""
        self.groups.addGroup('grptest1')
        self.groups.addGroup('grptest2')
        self.groups.editGroup('grptest2', ['Reviewer'], ['grptest1'], description='Sample group')
        self.groups.removeGroups(['grptest1', 'grptest2'])
        self.failIf('grptest2' in self.groups.listGroupIds())
        self.failIf('grptest1' in self.groups.listGroupIds())
        self.failIf('grptest2' in self.gruf.getGroupNames())
        self.failIf('grptest1' in self.gruf.getGroupNames())

    def test_setGroupOwnership(self):
        """Make the object 'object' owned by group 'group' (a portal_groupdata-ish object)"""
        pass

    def test_setGroupWorkspacesFolder(self):
        """ Set the location of the Group Workspaces folder by id.

        The Group Workspaces Folder contains all the group workspaces, just like the
        Members folder contains all the member folders.

        If anyone really cares, we can probably make the id work as a path as well,
        but for the moment it's only an id for a folder in the portal root, just like the
        corresponding MembershipTool functionality. """
        pass

    def test_getGroupWorkspacesFolderId(self):
        """ Get the Group Workspaces folder object's id.

        The Group Workspaces Folder contains all the group workspaces, just like the
        Members folder contains all the member folders. """
        pass

    def test_getGroupWorkspacesFolder(self):
        """ Get the Group Workspaces folder object.

        The Group Workspaces Folder contains all the group workspaces, just like the
        Members folder contains all the member folders. """
        pass

    def test_toggleGroupWorkspacesCreation(self):
        """ Toggles the flag for creation of a GroupWorkspaces folder upon first
        use of the group. """
        pass

    def test_getGroupWorkspacesCreationFlag(self):
        """Return the (boolean) flag indicating whether the Groups Tool will create a group workspace
        upon the next use of the group (if one doesn't exist). """
        pass

    def test_getGroupWorkspaceType(self):
        """Return the Type (as in TypesTool) to make the GroupWorkspace."""
        pass

    def test_setGroupWorkspaceType(self):
        """Set the Type (as in TypesTool) to make the GroupWorkspace. Expects the name of a Type."""
        pass

    def test_createGrouparea(self):
        """Create a space in the portal for the given group, much like member home
        folders."""
        pass

    def test_getGroupareaFolder(self):
        """Returns the object of the group's work area."""
        pass

    def test_getGroupareaURL(self):
        """Returns the full URL to the group's work area."""
        pass


class TestGroupDataTool(GroupTestCase, testInterface.TestInterface):
    __module__ = __name__
    klasses = (GroupDataTool.GroupDataTool,)
    ignore_interfaces = (
     ActionProviderBase.__implements__,)

    def test_wrapGroup(self):
        """Test group wrapping"""
        g1 = self.groups.getGroupById('g1')
        self.failUnlessEqual(g1.__class__.__name__, 'GroupData')
        self.failUnlessEqual(g1.getGroupName(), 'g1')
        g1 = self.groups.getGroupById('group_g1')
        self.failUnlessEqual(g1.__class__.__name__, 'GroupData')
        self.failUnlessEqual(g1.getGroupName(), 'g1')


class TestGroupData(GroupTestCase, testInterface.TestInterface):
    __module__ = __name__
    klasses = (GroupDataTool.GroupData,)
    ignore_interfaces = (
     ActionProviderBase.__implements__,)

    def test_setProperties(self, properties=None, **kw):
        """We set some properties on groups
        """
        g = self.groups.getGroupById('g1')
        g.setProperties({'email': 'test@toto.com', 'description': 'azer'})
        self.failUnlessEqual(g.getProperty('email'), 'test@toto.com')
        self.failUnlessEqual(g.getProperty('description'), 'azer')
        g.setProperties(email='other@toto.com', description='Bloub.')
        self.failUnlessEqual(g.getProperty('email'), 'other@toto.com')
        self.failIfEqual(g.getProperty('name'), 'Bloub.')
        g.setProperties(id='INVALID')
        self.failIfEqual(g.getProperty('id'), 'g1')

    def test_getProperty(self):
        g1 = self.groups.getGroupById('g1')
        self.failUnlessEqual(g1.getProperty('name'), 'g1')

    def test_getProperties(self):
        g1 = self.groups.getGroupById('g1')
        self.failUnlessEqual(g1.getProperties(), {'email': '', 'description': '', 'title': ''})
        g1.setProperties(email='test@toto.com', description='marih', title='Hello')
        self.failUnlessEqual(g1.getProperties(), {'email': 'test@toto.com', 'description': 'marih', 'title': 'Hello'})

    def test_getGroupId(self):
        g1 = self.groups.getGroupById('g1')
        self.failUnlessEqual(g1.getGroupId(), 'g1')

    def test_getMemberId(self):
        g1 = self.groups.getGroupById('g1')
        self.failUnlessEqual(g1.getMemberId(), 'g1')

    def test_getGroupName(self):
        g1 = self.groups.getGroupById('g1')
        self.failUnlessEqual(g1.getGroupName(), 'g1')

    def test_getGroupMembers(self):
        g1 = self.groups.getGroupById('g1')
        members = map(lambda x: x.getMemberId(), g1.getGroupMembers())
        members.sort()
        self.failUnlessEqual(members, [
         'u2', 'u3', 'u4'])
        g1.addMember('g2')
        members = map(lambda x: x.getMemberId(), g1.getGroupMembers())
        members.sort()
        self.failUnlessEqual(members, [
         'g2', 'u2', 'u3', 'u4'])

    def test_getAllGroupMembers(self):
        g1 = self.groups.getGroupById('g1')
        members = map(lambda x: x.getMemberId(), g1.getAllGroupMembers())
        members.sort()
        self.failUnlessEqual(members, [
         'u2', 'u3', 'u4'])
        g1.addMember('g2')
        members = map(lambda x: x.getMemberId(), g1.getAllGroupMembers())
        members.sort()
        self.failUnlessEqual(members, [
         'g2', 'u2', 'u3', 'u4', 'u5'])

    def test_getGroupMemberIds(self):
        g1 = self.groups.getGroupById('g1')
        members = g1.getGroupMemberIds()
        members.sort()
        self.failUnlessEqual(members, [
         'u2', 'u3', 'u4'])
        g1.addMember('g2')
        members = g1.getGroupMemberIds()
        members.sort()
        self.failUnlessEqual(members, [
         'g2', 'u2', 'u3', 'u4'])

    def test_getAllGroupMemberIds(self):
        g1 = self.groups.getGroupById('g1')
        members = g1.getAllGroupMemberIds()
        members.sort()
        self.failUnlessEqual(members, [
         'u2', 'u3', 'u4'])
        g1.addMember('g2')
        members = g1.getAllGroupMemberIds()
        members.sort()
        self.failUnlessEqual(members, [
         'g2', 'u2', 'u3', 'u4', 'u5'])

    def test_addMember(self):
        g1 = self.groups.getGroupById('g1')
        g1.addMember('u1')
        members = g1.getGroupMemberIds()
        members.sort()
        self.failUnlessEqual(members, [
         'u1', 'u2', 'u3', 'u4'])
        self.failUnlessRaises(ValueError, g1.addMember, 'bloubbloub')

    def test_removeMember(self):
        g1 = self.groups.getGroupById('g1')
        g1.removeMember('u2')
        members = g1.getGroupMemberIds()
        members.sort()
        self.failUnlessEqual(members, [
         'u3', 'u4'])
        self.failUnlessRaises(ValueError, g1.removeMember, 'bloubbloub')

    def test_getGroup(self):
        g1 = self.groups.getGroupById('g1')
        self.failUnlessEqual(g1.getGroup().__class__.__name__, 'GRUFGroup')


from AccessControl import Unauthorized
from AccessControl import Permissions
from Testing.ZopeTestCase import user_name

class TestMethodProtection(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.groups = self.portal.portal_groups
        self.groups.groupWorkspacesCreationFlag = 0
        self.groups.addGroup('foo')
        self.groupdata = self.groups.getGroupById('foo')

    def testAnonAddMember(self):
        self.logout()
        self.assertRaises(Unauthorized, self.groupdata.addMember, user_name)

    def testAnonRemoveMember(self):
        self.logout()
        self.assertRaises(Unauthorized, self.groupdata.removeMember, user_name)

    def testMemberAddMember(self):
        self.assertRaises(Unauthorized, self.groupdata.addMember, user_name)

    def testMemberRemoveMember(self):
        self.assertRaises(Unauthorized, self.groupdata.removeMember, user_name)

    def testManagerAddMember(self):
        self.setPermissions([Permissions.manage_users])
        self.groupdata.addMember(user_name)

    def testManagerRemoveMember(self):
        self.setPermissions([Permissions.manage_users])
        self.groupdata.addMember(user_name)
        self.groupdata.removeMember(user_name)


if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestGroupsTool))
        suite.addTest(unittest.makeSuite(TestGroupDataTool))
        suite.addTest(unittest.makeSuite(TestGroupData))
        suite.addTest(unittest.makeSuite(TestMethodProtection))
        return suite