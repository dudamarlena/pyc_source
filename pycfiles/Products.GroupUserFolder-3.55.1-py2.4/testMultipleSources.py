# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/tests/testMultipleSources.py
# Compiled at: 2008-05-20 04:51:55
"""

"""
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
import urllib
app = ZopeTestCase.app()
ZopeTestCase.utils.setupSiteErrorLog(app)
ZopeTestCase.close(app)
(host, port) = ZopeTestCase.utils.startZServer(4)
base = 'http://%s:%d/%s' % (host, port, ZopeTestCase.folder_name)
from AccessControl import getSecurityManager
from Products.GroupUserFolder.global_symbols import *
ZopeTestCase.installProduct('GroupUserFolder')
ZopeTestCase.installProduct('LDAPUserFolder')
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


class TestMultipleSources(ZopeTestCase.ZopeTestCase):
    __module__ = __name__

    def afterSetUp(self):
        """
        afterSetUp(self) => This method is called to create Folder with a GRUF inside.

        """
        self.folder.manage_delObjects(['acl_users'])
        self.folder.manage_addProduct['GroupUserFolder'].manage_addGroupUserFolder()
        self._setupUser()
        self.folder._addRole('r1')
        self.folder._addRole('r2')
        self.folder._addRole('r3')
        self.folder.acl_users._doAddGroup('g1', ())
        self.folder.acl_users._doAddGroup('g2', ('r1', ))
        self.folder.acl_users._doAddGroup('g3', ('r2', ))
        self.folder.acl_users._doAddGroup('g4', ('r2', 'r3'))
        self.folder.acl_users._doAddGroup('ng1', (), ('g1', ))
        self.folder.acl_users._doAddGroup('ng2', (), ('g2', 'g3'))
        self.folder.acl_users._doAddGroup('ng3', (), ('g2', 'ng2'))
        self.folder.acl_users._doAddGroup('ng4', ('r3', ), ('g2', 'ng2'))
        self.folder.acl_users._doAddGroup('ng5', (), ('g2', 'ng4'))
        self.folder.acl_users._doAddUser('manager', 'secret', ('Manager', ), (), ())
        self.folder.acl_users._doAddUser('u1', 'secret', (), (), ())
        self.folder.acl_users._doAddUser('u2', 'secret', (), (), ('g1', ))
        self.folder.acl_users._doAddUser('u3', 'secret', (), (), ('g1', 'g2'))
        self.folder.acl_users._doAddUser('u4', 'secret', (), (), ('g1', 'g2', 'g3'))
        self.folder.acl_users._doAddUser('u5', 'secret', ('r1', ), (), ('g2', 'g3'))
        self.folder.acl_users._doAddUser('u6', 'secret', ('r1', ), (), ('g3', ))
        self.folder.acl_users._doAddUser('u7', 'secret', ('r1', ), (), ('g4', ))
        self.folder.acl_users._doAddUser('u8', 'secret', (), (), ('ng1', ))
        self.folder.acl_users._doAddUser('u9', 'secret', (), (), ('g1', 'ng2'))
        self.folder.acl_users._doAddUser('u10', 'secret', (), (), ('ng2', 'ng3'))
        self.folder.acl_users._doAddUser('u11', 'secret', ('r3', ), (), ('ng2', 'ng3'))
        self.folder.manage_addProduct['OFSP'].manage_addFolder('lr')
        self.folder.lr.manage_addLocalRoles('group_g1', ('r3', ))
        self.folder.lr.manage_addLocalRoles('u3', ('r3', ))
        self.folder.lr.manage_addLocalRoles('u6', ('r3', ))
        self.folder.acl_users._doAddGroup('extranet', (), ())
        self.folder.acl_users._doAddGroup('intranet', (), ('extranet', ))
        self.folder.acl_users._doAddGroup('compta', (), ('intranet', 'extranet'))

    def build(self):
        self.folder.acl_users.addUserSource('manage_addProduct/OFSP/manage_addUserFolder')

    def test01addSources(self):
        """Add a few user sources"""
        self.folder.acl_users.addUserSource('manage_addProduct/OFSP/manage_addUserFolder')
        self.failUnless('Users01' in self.folder.acl_users.objectIds())
        self.failUnless(self.folder.acl_users.Users01.getId() == 'Users01')
        self.failUnless('acl_users' in self.folder.acl_users.Users01.objectIds())
        self.failUnless(not self.folder.acl_users.listUserSources()[(-1)].getUserNames())

    def test02getDefaultSource(self):
        """Test default source retreiving"""
        self.build()
        self.failUnless(self.folder.acl_users.getDefaultUserSource().getId() == 'acl_users')

    def test03userFetching(self):
        """Test user creation & fetching"""
        self.build()
        self.failUnless(self.folder.acl_users.listUserSources()[(-1)].aq_parent.id == 'Users01')
        self.failUnless(self.folder.acl_users.listUserSources()[(-1)].meta_type == 'User Folder')
        self.folder.acl_users.listUserSources()[(-1)]._doAddUser('U1_01', 'secret', (), ())
        self.failUnless(self.folder.acl_users.listUserSources()[(-1)].getUserNames() == ['U1_01'])
        U1 = self.folder.acl_users.getUser('U1_01')
        self.folder.acl_users.getUser('u1')
        self.failUnless(self.folder.acl_users.getUser('U1_01').getUserSourceId() == 'Users01')
        self.failUnless(self.folder.acl_users.getUnwrappedUser('U1_01').name == 'U1_01')

    def test04ChangeUserRole(self):
        """Test if it possible to change a user's role using the sources API"""
        self.setRoles(['Manager'])
        user = getSecurityManager().getUser()
        Log(LOG_DEBUG, user.getRoles())
        self.failUnless(user.has_role('Manager'))

    def test05AvailableTypes(self):
        """test available user folders"""
        self.setRoles(['Manager'])
        self.failUnless(getSecurityManager().getUser().has_role('Manager'))
        sources = self.folder.acl_users.listAvailableUserSources(filter_permissions=0, filter_classes=1)
        self.failUnless(('User Folder', 'manage_addProduct/OFSP/manage_addUserFolder') in sources, 'There should only have one UF, not %s' % (sources,))

    def test06LUFSource(self):
        gruf = self.folder.acl_users
        self.failUnlessEqual(gruf.getLUFSource(), None)
        try:
            gruf.replaceUserSource('Users', 'manage_addProduct/LDAPUserFolder/manage_addLDAPUserFolder')
        except AttributeError:
            return

        self.failUnlessEqual(gruf.getLUFSource().meta_type, 'LDAPUserFolder')
        gruf.addUserSource('manage_addProduct/OFSP/manage_addUserFolder')
        self.failUnlessEqual(gruf.getLUFSource().meta_type, 'LDAPUserFolder')
        return


if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestMultipleSources))
        return suite