# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/GRUFFolder.py
# Compiled at: 2008-05-20 04:51:58
__doc__ = '\n\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from Globals import MessageDialog, DTMLFile
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item
from OFS.PropertyManager import PropertyManager
from OFS import ObjectManager, SimpleItem
from DateTime import DateTime
from App import ImageFile
import DynaList, AccessControl.Role, webdav.Collection, Products, os, string, shutil, random

def manage_addGRUFUsers(self, id='Users', dtself=None, REQUEST=None, **ignored):
    """ """
    f = GRUFUsers(id)
    self = self.this()
    try:
        self._setObject(id, f)
    except:
        return MessageDialog(title='Item Exists', message='This object already contains a GRUFUsers Folder', action='%s/manage_main' % REQUEST['URL1'])

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')
    return


def manage_addGRUFGroups(self, id='Groups', dtself=None, REQUEST=None, **ignored):
    """ """
    f = GRUFGroups(id)
    self = self.this()
    try:
        self._setObject(id, f)
    except:
        return MessageDialog(title='Item Exists', message='This object already contains a GRUFGroups Folder', action='%s/manage_main' % REQUEST['URL1'])

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')
    return


class GRUFFolder(ObjectManager.ObjectManager, SimpleItem.Item):
    __module__ = __name__
    isAnObjectManager = 1
    isPrincipiaFolderish = 1
    manage_main = DTMLFile('dtml/GRUFFolder_main', globals())
    manage_options = ({'label': 'Contents', 'action': 'manage_main'},) + SimpleItem.Item.manage_options
    security = ClassSecurityInfo()

    def __creatable_by_emergency_user__(self):
        return 1

    def __init__(self, id=None):
        if id:
            self.id = id
        else:
            self.id = self.default_id

    def getId(self):
        if self.id:
            return self.id
        else:
            return self.default_id

    def getUserSourceId(self):
        return self.getId()

    def isValid(self):
        """
        isValid(self,) => Return true if an acl_users is inside
        """
        if 'acl_users' in self.objectIds():
            return 1
        return

    security.declarePublic('header_text')

    def header_text(self):
        """
        header_text(self,) => Text that appears in the content's
                              view heading zone
        """
        return ''

    def getUserFolder(self):
        """
        getUserFolder(self,) => get the underlying user folder, UNRESTRICTED !
        """
        if 'acl_users' not in self.objectIds():
            raise 'ValueError', 'Please put an acl_users in %s before using GRUF' % (self.getId(),)
        return self.restrictedTraverse('acl_users')

    def getUserNames(self):
        """
        getUserNames(self,) => None

        We override this to prevent SimpleUserFolder to use GRUF's getUserNames() method.
        It's, of course, still possible to override a getUserNames method with SimpleUserFolder:
        just call it 'new_getUserNames'.
        """
        if 'new_getUserNames' in self.objectIds():
            return self.unrestrictedTraverse('new_getUserNames')()
        return ()


class GRUFUsers(GRUFFolder):
    """
    GRUFUsers : GRUFFolder that holds users
    """
    __module__ = __name__
    meta_type = 'GRUFUsers'
    default_id = 'Users'
    manage_options = GRUFFolder.manage_options

    class C__ac_roles__(Persistent, Implicit, DynaList.DynaList):
        """
        __ac_roles__ dynastring.
        Do not forget to set _target to class instance.

        XXX DynaList is surely not efficient but it's the only way
        I found to do what I wanted easily. Someone should take
        a look to PerstList instead to see if it's possible
        to do the same ? (ie. having a list which elements are
        the results of a method call).

        However, even if DynaList is not performant, it's not
        a critical point because this list is meant to be
        looked at only when a User object is looked at INSIDE
        GRUF (especially to set groups a user belongs to).
        So in practice only used within ZMI.
        """
        __module__ = __name__

        def data(self):
            return self.userdefined_roles()

    ac_roles = C__ac_roles__()
    __ac_roles__ = ac_roles
    enabled = 1

    def enableSource(self):
        """enableSource(self,) => Set enable status to 1
        """
        self.enabled = 1

    def disableSource(self):
        """disableSource(self,) => explicit ;)
        """
        self.enabled = None
        return

    def isEnabled(self):
        """
        Return true if enabled (surprisingly)
        """
        return not not self.enabled

    def header_text(self):
        """
        header_text(self,) => Text that appears in the content's view
                              heading zone
        """
        if 'acl_users' not in self.objectIds():
            return 'Please put an acl_users here before ever starting to use this object.'
        ret = "In this folder, groups are seen as ROLES from user's\n                 view. To put a user into a group, affect him a role\n                 that matches his group.<br />"
        return ret

    def listGroups(self):
        """
        listGroups(self,) => return a list of groups defined as roles
        """
        return self.Groups.restrictedTraverse('listGroups')()

    def userdefined_roles(self):
        """Return list of user-defined roles"""
        return self.listGroups()


class GRUFGroups(GRUFFolder):
    """
    GRUFGroups : GRUFFolder that holds groups
    """
    __module__ = __name__
    meta_type = 'GRUFGroups'
    default_id = 'Groups'
    _group_prefix = 'group_'

    class C__ac_roles__(Persistent, Implicit, DynaList.DynaList):
        """
        __ac_roles__ dynastring.
        Do not forget to set _target to class instance.

        XXX DynaList is surely not efficient but it's the only way
        I found to do what I wanted easily. Someone should take
        a look to PerstList instead to see if it's possible
        to do the same ? (ie. having a list which elements are
        the results of a method call).

        However, even if DynaList is not performant, it's not
        a critical point because this list is meant to be
        looked at only when a User object is looked at INSIDE
        GRUF (especially to set groups a user belongs to).
        So in practice only used within ZMI.
        """
        __module__ = __name__

        def data(self):
            return self.userdefined_roles()

    ac_roles = C__ac_roles__()
    __ac_roles__ = ac_roles

    def header_text(self):
        """
        header_text(self,) => Text that appears in the content's
                              view heading zone
        """
        ret = ''
        if 'acl_users' not in self.objectIds():
            return 'Please put an acl_users here before ever starting to use this object.'
        return ret

    def _getGroup(self, id):
        """
        _getGroup(self, id) => same as getUser() but... with a group :-)
        This method will return an UNWRAPPED object
        """
        return self.acl_users.getUser(id)

    def listGroups(self, prefixed=1):
        """
        Return a list of available groups.
        Group names are prefixed !
        """
        if not prefixed:
            return self.acl_users.getUserNames()
        else:
            ret = []
            for grp in self.acl_users.getUserNames():
                ret.append('%s%s' % (self._group_prefix, grp))

            return ret

    def userdefined_roles(self):
        """Return list of user-defined roles"""
        return self.listGroups()


InitializeClass(GRUFUsers)
InitializeClass(GRUFGroups)