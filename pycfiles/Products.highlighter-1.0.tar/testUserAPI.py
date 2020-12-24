# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/tests/testUserAPI.py
# Compiled at: 2008-05-20 04:51:55
__doc__ = '\n\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
from AccessControl.Permissions import access_contents_information, view, add_documents_images_and_files, change_images_and_files, view_management_screens
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager, getSecurityManager
from AccessControl import Unauthorized
from AccessControl.User import UnrestrictedUser
import urllib, string
app = ZopeTestCase.app()
ZopeTestCase.utils.setupSiteErrorLog(app)
ZopeTestCase.close(app)
from Products.GroupUserFolder import GRUFUser
from Interface import Verify
ZopeTestCase.installProduct('GroupUserFolder')
import GRUFTestCase, testInterface
from Log import *

class TestUserFolderAPI(GRUFTestCase.GRUFTestCase, testInterface.TestInterface):
    __module__ = __name__
    klasses = (
     GRUFUser.GRUFUser, GRUFUser.GRUFGroup)

    def test03ClassSecurityInfo(self):
        """We inhibit this test: class security info is not managed this way with user objects
        """
        pass

    def test_getId(self):
        u = self.gruf.getUser('u1')
        self.failUnless(u.getId() == 'u1')
        u = self.gruf.getUser('group_g1')
        self.failUnless(u.getId() == 'group_g1')

    def test_getUserName(self):
        u = self.gruf.getUser('u1')
        self.failUnless(u.getUserName() == 'u1')
        u = self.gruf.getUser('group_g1')
        self.failUnless(u.getUserName() == 'g1')

    def test_getName(self):
        u = self.gruf.getUser('u1')
        self.failUnless(u.getUserName() == 'u1')
        u = self.gruf.getUser('group_g1')
        self.failUnless(u.getUserName() == 'g1')

    def test_getRoles(self):
        u = self.gruf.getUser('u5')
        r = list(u.getRoles())
        r.sort()
        Log(LOG_DEBUG, r)
        self.failUnless(r == ['Authenticated', 'r1', 'r2'])

    def test_setRoles(self):
        u = self.gruf.getUser('u5')
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r1', 'r2'])
        u.setRoles(['r3', 'r2', 'r1'])
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r1', 'r2', 'r3'])
        try:
            u.setRoles(['r3', 'r2', 'r1', 'bloub'])
        except ValueError:
            pass
        else:
            raise AssertionError, 'Should raise a ValueError here'

        u.setRoles([])
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r1', 'r2'])
        u = self.gruf.getUser('u6')
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r1', 'r2'])
        u.setRoles([])
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r2'])

    def test_addRole(self):
        u = self.gruf.getUser('u5')
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r1', 'r2'])
        u.addRole('r3')
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r1', 'r2', 'r3'])
        try:
            u.addRole('bloub')
        except ValueError:
            pass
        else:
            raise AssertionError, 'Should raise a ValueError here'

    def test_removeRole(self):
        u = self.gruf.getUser('u6')
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r1', 'r2'])
        u.removeRole('r1')
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r2'])
        u.removeRole('r1')
        r = list(u.getRoles())
        r.sort()
        self.failUnless(r == ['Authenticated', 'r2'])
        u.removeRole('r2')
        r = list(u.getRoles())
        r.sort()
        Log(LOG_DEBUG, r)
        self.failUnless(r == ['Authenticated', 'r2'])

    def test_getRolesInContext(self):
        r = self.gruf.getUser('u2').getRolesInContext(self.gruf_folder.lr)
        self.failUnless('r3' in r)
        r = self.gruf.getUser('u3').getRolesInContext(self.gruf_folder.lr)
        self.failUnless('r1' in r)
        self.failUnless('r3' in r)

    def test_has_permission(self):
        pass

    def test_allowed(self):
        pass

    def test_has_role(self):
        u = self.gruf.getUser('u2')
        self.failUnless(u.has_role('r3', self.gruf_folder.lr))

    def test_isGroup(self):
        u = self.gruf.getUser('u1')
        self.failUnless(not u.isGroup())
        u = self.gruf.getUser('u2')
        self.failUnless(not u.isGroup())
        u = self.gruf.getUser('g1')
        self.failUnless(u.isGroup())
        u = self.gruf.getUser('ng2')
        self.failUnless(u.isGroup())
        u = self.gruf.getUser('g3')
        self.failUnless(u.isGroup())

    def test_getGroupNames(self):
        u = self.gruf.getUser('u2')
        g = u.getGroupNames()
        g.sort()
        self.failUnless(g == ['g1'])
        u = self.gruf.getUser('u1')
        g = u.getGroupNames()
        g.sort()
        self.failUnless(g == [])
        u = self.gruf.getUser('ng1')
        g = u.getGroupNames()
        g.sort()
        self.failUnless(g == ['g1'])
        u = self.gruf.getUser('u10')
        g = u.getGroupNames()
        g.sort()
        self.failUnless(g == ['ng2', 'ng3'])

    def test_getGroupIds(self):
        u = self.gruf.getUser('u2')
        g = u.getGroupIds()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u1')
        g = u.getGroupIds()
        g.sort()
        self.failUnless(g == [])
        u = self.gruf.getUser('ng1')
        g = u.getGroupIds()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u10')
        g = u.getGroupIds()
        g.sort()
        self.failUnless(g == ['group_ng2', 'group_ng3'])

    def test_getGroups(self):
        u = self.gruf.getUser('u2')
        g = u.getGroups()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u1')
        g = u.getGroups()
        g.sort()
        self.failUnless(g == [])
        u = self.gruf.getUser('ng1')
        g = u.getGroups()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u10')
        g = u.getGroups()
        g.sort()
        self.failUnless(g == ['group_g2', 'group_g3', 'group_ng2', 'group_ng3'])

    def test_getImmediateGroups(self):
        u = self.gruf.getUser('u2')
        g = u.getImmediateGroups()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u1')
        g = u.getImmediateGroups()
        g.sort()
        self.failUnless(g == [])
        u = self.gruf.getUser('ng1')
        g = u.getImmediateGroups()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u10')
        g = u.getImmediateGroups()
        g.sort()
        self.failUnless(g == ['group_ng2', 'group_ng3'], u.getImmediateGroups())

    def test_getAllGroupIds(self):
        u = self.gruf.getUser('u2')
        g = u.getAllGroupIds()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u1')
        g = u.getAllGroupIds()
        g.sort()
        self.failUnless(g == [])
        u = self.gruf.getUser('ng1')
        g = u.getAllGroupIds()
        g.sort()
        self.failUnless(g == ['group_g1'])
        u = self.gruf.getUser('u10')
        g = u.getAllGroupIds()
        g.sort()
        self.failUnless(g == ['group_g2', 'group_g3', 'group_ng2', 'group_ng3'])

    def test_getAllGroupNames(self):
        u = self.gruf.getUser('u2')
        g = u.getAllGroupNames()
        g.sort()
        self.failUnless(g == ['g1'])
        u = self.gruf.getUser('u1')
        g = u.getAllGroupNames()
        g.sort()
        self.failUnless(g == [])
        u = self.gruf.getUser('ng1')
        g = u.getAllGroupNames()
        g.sort()
        self.failUnless(g == ['g1'])
        u = self.gruf.getUser('u10')
        g = u.getAllGroupNames()
        g.sort()
        self.failUnless(g == ['g2', 'g3', 'ng2', 'ng3'])

    def test_isInGroup(self):
        u = self.gruf.getUser('u2')
        self.failUnless(u.isInGroup('group_g1'))
        self.failUnless(not u.isInGroup('g1'))
        u = self.gruf.getUser('u1')
        self.failUnless(not u.isInGroup('group_g1'))
        u = self.gruf.getUser('ng1')
        self.failUnless(u.isInGroup('group_g1'))
        u = self.gruf.getUser('u10')
        self.failUnless(u.isInGroup('group_g2'))
        self.failUnless(u.isInGroup('group_g3'))
        self.failUnless(u.isInGroup('group_ng2'))
        self.failUnless(u.isInGroup('group_ng3'))

    def test_setGroups(self):
        self.gruf.userFolderAddUser(name='created_user', password='secret', groups=[], roles=(), domains=())
        u = self.gruf.getUser('created_user')
        u.setGroups(['g1', 'g2'])
        self.compareGroups('created_user', ['g1', 'g2'])
        u.setGroups([])
        self.compareGroups('created_user', [])
        u.setGroups(['group_g1', 'group_g2'])
        self.compareGroups('created_user', ['g1', 'g2'])
        try:
            u.setGroups(['group_g1', 'group_g2', 'bloub'])
        except ValueError:
            pass
        else:
            raise AssertionError, 'Should raise ValueError'

    def test_addGroup(self):
        u = self.gruf.getUser('u1')
        self.failUnless(u.getGroups() == [])
        u.addGroup('g3')
        self.failUnless(u.getGroups() == ['group_g3'])
        u.addGroup('group_g2')
        r = u.getGroups()
        r.sort()
        self.failUnless(r == ['group_g2', 'group_g3'])

    def test_removeGroup(self):
        u = self.gruf.getUser('u1')
        u.addGroup('group_g3')
        u.addGroup('group_g2')
        r = u.getGroups()
        r.sort()
        self.failUnless(r == ['group_g2', 'group_g3'])
        u.removeGroup('group_g3')
        Log(LOG_DEBUG, u.getGroups())
        self.failUnless(u.getGroups() == ['group_g2'])
        u.removeGroup('group_g2')
        self.failUnless(u.getGroups() == [])

    def test_getRealId(self):
        u = self.gruf.getUser('u1')
        self.failUnless(u.getRealId() == 'u1')
        u = self.gruf.getUser('g1')
        self.failUnless(u.getRealId() == 'g1')
        u = self.gruf.getUser('group_g1')
        self.failUnless(u.getRealId() == 'g1')

    def test_getDomains(self):
        """Return the list of domain restrictions for a user"""
        self.gruf.userFolderAddUser('test_crea', 'secret', [], [
         'a', 'b', 'c'], [])
        u = self.gruf.getUser('test_crea')
        d = list(u.getDomains())
        d.sort()
        self.failUnless(d == ['a', 'b', 'c'])

    def test_setPassword(self):
        user = self.gruf.getUser('u1')
        self.failUnless(user.authenticate('secret', self.app.REQUEST))
        user.setPassword('marih')
        self.failUnless(not user.authenticate('secret', self.app.REQUEST))
        self.failUnless(user.authenticate('marih', self.app.REQUEST))
        u = self.gruf.getUser('g1')
        try:
            u.setPassword('bloub')
        except AttributeError:
            pass
        else:
            raise AssertionError, 'Password change must be prohibited for groups'

    def test_setDomains(self):
        u = self.gruf.getUser('u1')
        self.failUnless(not u.getDomains())
        u.setDomains(['d1', 'd2', 'd3'])
        d = list(u.getDomains())
        d.sort()
        self.failUnless(d == ['d1', 'd2', 'd3'])
        u.setDomains([])
        self.failUnless(tuple(u.getDomains()) == ())
        u.setDomains(['xxx'])
        self.failUnless(tuple(u.getDomains()) == ('xxx', ))

    def test_addDomain(self):
        """..."""
        pass

    def test_removeDomain(self):
        """..."""
        pass

    def test_getMemberIds(self):
        u = self.gruf.getGroup('ng2')
        ulist = u.getMemberIds()
        ulist.sort()
        self.failUnless(ulist == ['group_ng3', 'group_ng4', 'group_ng5', 'u10', 'u11', 'u9'])

    def test_getUserMemberIds(self):
        u = self.gruf.getGroup('ng2')
        ulist = u.getUserMemberIds()
        ulist.sort()
        self.failUnless(ulist == ['u10', 'u11', 'u9'])
        u = self.gruf.getGroup('g2')
        ulist = u.getUserMemberIds()
        ulist.sort()
        self.failUnless(ulist == ['u10', 'u11', 'u3', 'u4', 'u5', 'u9'])

    def test_getGroupMemberIds(self):
        u = self.gruf.getGroup('ng2')
        ulist = u.getGroupMemberIds()
        ulist.sort()
        self.failUnless(ulist == ['group_ng3', 'group_ng4', 'group_ng5'])

    def test_hasMember(self):
        self.failUnless(self.gruf.getGroup('g2').hasMember('u4'))
        self.failUnless(self.gruf.getGroup('g2').hasMember('group_ng2'))

    def test_addMember(self):
        g = self.gruf.getGroup('ng3')
        self.failUnless('u1' not in g.getMemberIds())
        g.addMember('u1')
        self.failUnless('u1' in g.getMemberIds())

    def test_removeMember(self):
        g = self.gruf.getGroup('ng3')
        self.failUnless('u1' not in g.getMemberIds())
        g.addMember('u1')
        self.failUnless('u1' in g.getMemberIds())
        g.removeMember('u1')
        self.failUnless('u1' not in g.getMemberIds())
        g2 = self.gruf.getGroup('g2')
        ng5 = self.gruf.getGroup('ng5')
        self.failUnless('group_ng1' not in ng5.getMemberIds())
        self.failUnless('group_ng1' not in g2.getMemberIds())
        ng5.addMember('ng1')
        self.failUnless('group_ng1' in ng5.getMemberIds())
        self.failUnless('group_ng1' in g2.getMemberIds())
        ng5.removeMember('ng1')
        self.failUnless('group_ng1' not in ng5.getMemberIds())
        self.failUnless('group_ng1' not in g2.getMemberIds())

    def test_getProperty(self):
        """Will raise for regular user folders
        """
        try:
            self.gruf.getUser('u1').getProperty('email')
        except:
            pass
        else:
            raise AssertionError, 'Should raise'

    def test_hasProperty(self):
        self.failUnless(not self.gruf.getUser('u1').hasProperty('email'))

    def test_setProperty(self):
        try:
            self.gruf.getUser('u1').setProperty('email', 'test@test.com')
        except NotImplementedError:
            pass
        else:
            raise AssertionError, 'Should raise here.'


if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestUserFolderAPI))
        return suite