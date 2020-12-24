# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/tests/testLDAPUserFolder.py
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
import urllib
app = ZopeTestCase.app()
ZopeTestCase.utils.setupSiteErrorLog(app)
ZopeTestCase.close(app)
(host, port) = ZopeTestCase.utils.startZServer(4)
base = 'http://%s:%d/%s' % (host, port, ZopeTestCase.folder_name)
from Products.GroupUserFolder.interfaces import IUserFolder
from Interface import Verify
ZopeTestCase.installProduct('GroupUserFolder')
ZopeTestCase.installProduct('LDAPUserFolder')
import GRUFTestCase, testGroupUserFolderAPI
from Log import *
try:
    from LDAPconfig import defaults
except ImportError:
    Log(LOG_ERROR, "\n    To perform this test case, you must provide a 'LDAPconfig.py' file with the following structure:\n\ndefaults = { 'title'  : 'LDAP User Folder'\n           , 'server' : 'localhost:389'\n           , 'login_attr' : 'cn'\n           , 'uid_attr': 'cn'\n           , 'users_base' : 'ou=people,dc=dataflake,dc=org'\n           , 'users_scope' : 2\n           , 'roles' : 'Anonymous'\n           , 'groups_base' : 'ou=groups,dc=dataflake,dc=org'\n           , 'groups_scope' : 2\n           , 'binduid' : 'cn=Manager,dc=dataflake,dc=org'\n           , 'bindpwd' : 'mypass'\n           , 'binduid_usage' : 1\n           , 'rdn_attr' : 'cn'\n           , 'local_groups' : 1                 # Keep this true\n           , 'use_ssl' : 0\n           , 'encryption' : 'SHA'\n           , 'read_only' : 0\n           }\n\n    Of course, you've got to replace all values by some relevant ones for your project.\n    This test case won't complete without.\n\n    NEVER PUT THIS FILE INTO YOUR CVS ! Unless you want your password to be publicly known...\n    ")
    ldapuf = False
else:
    ldapuf = True
    dg = defaults.get

class TestLDAPUserFolderBasics(GRUFTestCase.GRUFTestCase):
    """
    Basic LDAPUserFolder binding
    This test just creates a LDAPUF connexion for the user source and performs a few API tests.
    Heavy LDAP testing is delegated to TestLDAPUserFolder class.
    """
    __module__ = __name__

    def gruf_sources_setup(self):
        """
        Basic LDAP initialization inside gruf's user source
        """
        self.gruf.replaceUserSource('Users', 'manage_addProduct/LDAPUserFolder/manage_addLDAPUserFolder')
        self.gruf.Users.acl_users.manage_edit(title=dg('title'), login_attr=dg('login_attr'), uid_attr=dg('uid_attr'), users_base=dg('users_base'), users_scope=dg('users_scope'), roles=dg('roles'), obj_classes='top,inetOrgPerson', groups_base=dg('groups_base'), groups_scope=dg('groups_scope'), binduid=dg('binduid'), bindpwd=dg('bindpwd'), binduid_usage=dg('binduid_usage'), rdn_attr=dg('rdn_attr'), local_groups=dg('local_groups'), encryption=dg('encryption'), read_only=dg('read_only'))
        self.delete_created_users()

    def test01_LDAPUp(self):
        """Ensure LDAP is up and running
        """
        self.gruf.Users.acl_users.getUsers()


class TestLDAPUserFolderAPI(TestLDAPUserFolderBasics, testGroupUserFolderAPI.TestGroupUserFolderAPI):
    """
    Whole API test for GRUF+LDAP

    Users stored in LDAP
    Groups stored in ZODB
    """
    __module__ = __name__

    def test_getPureUsers(self):
        """
        The original test didn't work because of LDAPUF's cache -> we disable
        """
        pass

    def test_getUsers(self):
        """
        The original test didn't work because of LDAPUF's cache -> we disable
        """
        pass

    def test_userSetDomains(self):
        """
        LDAPUF has no domain support
        """
        pass

    def test_setProperty(self):
        """Set user's properties
        """
        u1 = self.gruf.getUser('u1')
        u1.setProperty('sn', 'Second Name Value')
        self.failUnless(u1.getProperty('sn') == 'Second Name Value', u1.getProperty('sn'))

    def test_searchUsersByAttribute(self):
        self.failUnlessEqual(self.gruf.searchUsersByAttribute(defaults['login_attr'], 'u3'), [
         'u3'])
        self.failUnlessEqual(self.gruf.searchUsersByAttribute(defaults['login_attr'], 'U3'), [
         'u3'])
        s = self.gruf.searchUsersByAttribute(defaults['login_attr'], 'U')
        s.sort()
        self.failUnlessEqual(s, [
         'u1', 'u10', 'u11', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7', 'u8', 'u9'])


if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        if ldapuf:
            suite.addTest(unittest.makeSuite(TestLDAPUserFolderAPI))
        return suite