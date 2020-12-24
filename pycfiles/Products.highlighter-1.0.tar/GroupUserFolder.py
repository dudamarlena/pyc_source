# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/GroupUserFolder.py
# Compiled at: 2008-05-20 04:51:58
__doc__ = '\nGroupUserFolder product\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from Globals import MessageDialog, DTMLFile
from AccessControl import ClassSecurityInfo
from AccessControl import Permissions
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Globals import InitializeClass
from Acquisition import aq_base, aq_inner, aq_parent
from Acquisition import Implicit
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item
from OFS.PropertyManager import PropertyManager
import OFS
from OFS import ObjectManager, SimpleItem
from DateTime import DateTime
from App import ImageFile
from Products.PageTemplates import PageTemplateFile
import AccessControl.Role, webdav.Collection, Products, os, string, sys, time, math, random
from global_symbols import *
import AccessControl.User, GRUFFolder, GRUFUser
from Products.PageTemplates import PageTemplateFile
import class_utility
from Products.GroupUserFolder import postonly
from interfaces.IUserFolder import IUserFolder
_marker = []

def unique(sequence, _list=0):
    """Make a sequence a list of unique items"""
    uniquedict = {}
    for v in sequence:
        uniquedict[v] = 1

    if _list:
        return list(uniquedict.keys())
    return tuple(uniquedict.keys())


def manage_addGroupUserFolder(self, dtself=None, REQUEST=None, **ignored):
    """ Factory method that creates a UserFolder"""
    f = GroupUserFolder()
    self = self.this()
    try:
        self._setObject('acl_users', f)
    except:
        return MessageDialog(title='Item Exists', message='This object already contains a User Folder', action='%s/manage_main' % REQUEST['URL1'])

    self.__allow_groups__ = f
    self.acl_users._post_init()
    self.acl_users.Users.manage_addUserFolder()
    self.acl_users.Groups.manage_addUserFolder()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')
    return


class GroupUserFolder(OFS.ObjectManager.ObjectManager, AccessControl.User.BasicUserFolder):
    """
    GroupUserFolder => User folder with groups management
    """
    __module__ = __name__
    meta_type = 'Group User Folder'
    id = 'acl_users'
    title = 'Group-aware User Folder'
    __implements__ = (
     IUserFolder,)

    def __creatable_by_emergency_user__(self):
        return 1

    isAnObjectManager = 1
    isPrincipiaFolderish = 1
    isAUserFolder = 1
    security = ClassSecurityInfo()
    manage_options = ({'label': 'Overview', 'action': 'manage_overview'}, {'label': 'Sources', 'action': 'manage_GRUFSources'}, {'label': 'LDAP Wizard', 'action': 'manage_wizard'}, {'label': 'Groups', 'action': 'manage_groups'}, {'label': 'Users', 'action': 'manage_users'}, {'label': 'Audit', 'action': 'manage_audit'}) + OFS.ObjectManager.ObjectManager.manage_options + RoleManager.manage_options + Item.manage_options
    manage_main = OFS.ObjectManager.ObjectManager.manage_main
    manage_overview = PageTemplateFile.PageTemplateFile('dtml/GRUF_overview', globals())
    manage_audit = PageTemplateFile.PageTemplateFile('dtml/GRUF_audit', globals())
    manage_wizard = PageTemplateFile.PageTemplateFile('dtml/GRUF_wizard', globals())
    manage_groups = PageTemplateFile.PageTemplateFile('dtml/GRUF_groups', globals())
    manage_users = PageTemplateFile.PageTemplateFile('dtml/GRUF_users', globals())
    manage_newusers = PageTemplateFile.PageTemplateFile('dtml/GRUF_newusers', globals())
    manage_GRUFSources = PageTemplateFile.PageTemplateFile('dtml/GRUF_contents', globals())
    manage_user = PageTemplateFile.PageTemplateFile('dtml/GRUF_user', globals())
    __ac_permissions__ = (
     (
      'Manage users', ('manage_users', 'user_names', 'setDomainAuthenticationMode')),)
    user_color = '#006600'
    group_color = '#000099'
    role_color = '#660000'
    img_user = ImageFile.ImageFile('www/GRUFUsers.gif', globals())
    img_group = ImageFile.ImageFile('www/GRUFGroups.gif', globals())
    security.declarePublic('hasUsers')

    def hasUsers(self):
        """
        From Zope 2.7's User.py:
        This is not a formal API method: it is used only to provide
        a way for the quickstart page to determine if the default user
        folder contains any users to provide instructions on how to
        add a user for newbies.  Using getUserNames or getUsers would have
        posed a denial of service risk.
        In GRUF, this method always return 1."""
        return 1

    security.declareProtected(Permissions.manage_users, 'user_names')

    def user_names(self):
        """
        user_names() => return user IDS and not user NAMES !!!
        Due to a Zope inconsistency, the Role.get_valid_userids return user names
        and not user ids - which is bad. As GRUF distinguishes names and ids, this
        will cause it to break, especially in the listLocalRoles form. So we change
        user_names() behaviour so that it will return ids and not names.
        """
        return self.getUserIds()

    security.declareProtected(Permissions.manage_users, 'getUserNames')

    def getUserNames(self, __include_groups__=1, __include_users__=1, __groups_prefixed__=0):
        """
        Return a list of all possible user atom names in the system.
        Groups will be returned WITHOUT their prefix by this method.
        So, there might be a collision between a user name and a group name.
        [NOTA: This method is time-expensive !]
        """
        if __include_users__:
            LogCallStack(LOG_DEBUG, 'This call can be VERY expensive!')
        names = []
        ldap_sources = []
        if __include_users__:
            for src in self.listUserSources():
                names.extend(src.getUserNames())

        if __include_groups__:
            if 'acl_users' in self._getOb('Groups').objectIds():
                names.extend(self.Groups.listGroups(prefixed=__groups_prefixed__))
            for ldapuf in ldap_sources:
                if ldapuf._local_groups:
                    continue
                for g in ldapuf.getGroups(attr=LDAP_GROUP_RDN):
                    if __groups_prefixed__:
                        names.append('%s%s' % (GROUP_PREFIX, g))
                    else:
                        names.append(g)

        return unique(names, _list=1)

    security.declareProtected(Permissions.manage_users, 'getUserIds')

    def getUserIds(self):
        """
        Return a list of all possible user atom ids in the system.
        WARNING: Please see the id Vs. name consideration at the
        top of this document. So, groups will be returned
        WITH their prefix by this method
        [NOTA: This method is time-expensive !]
        """
        return self.getUserNames(__groups_prefixed__=1)

    security.declareProtected(Permissions.manage_users, 'getUsers')

    def getUsers(self, __include_groups__=1, __include_users__=1):
        """Return a list of user and group objects.
        In case of some UF implementations, the returned object may only be a subset
        of all possible users.
        In other words, you CANNOT assert that len(getUsers()) equals len(getUserNames()).
        With cache-support UserFolders, such as LDAPUserFolder, the getUser() method will
        return only cached user objects instead of fetching all possible users.
        """
        Log(LOG_DEBUG, 'getUsers')
        ret = []
        names_set = {}
        isUserProcessed = names_set.has_key
        if __include_groups__:
            for u in self._getOb('Groups').acl_users.getUsers():
                if not u:
                    continue
                name = u.getId()
                if isUserProcessed(name):
                    continue
                names_set[name] = True
                ret.append(GRUFUser.GRUFGroup(u, self, isGroup=1, source_id='Groups').__of__(self))

        if __include_users__:
            for src in self.listUserSources():
                for u in src.getUsers():
                    if not u:
                        continue
                    name = u.getId()
                    if isUserProcessed(name):
                        continue
                    names_set[name] = True
                    ret.append(GRUFUser.GRUFUser(u, self, source_id=src.getUserSourceId(), isGroup=0).__of__(self))

        return tuple(ret)

    security.declareProtected(Permissions.manage_users, 'getUser')

    def getUser(self, name, __include_users__=1, __include_groups__=1, __force_group_id__=0):
        """
        Return the named user object or None.
        User have precedence over group.
        If name is None, getUser() will return None.
        """
        if name is None:
            return
        if 'acl_users' not in self._getOb('Groups').objectIds():
            return
        if __include_groups__ and name.startswith(GROUP_PREFIX):
            id = name[GROUP_PREFIX_LEN:]
            u = self._getOb('Groups')._getGroup(id)
            if u:
                ret = GRUFUser.GRUFGroup(u, self, isGroup=1, source_id='Groups').__of__(self)
                return ret
        if __include_users__:
            for src in self.listUserSources():
                u = src.getUser(name)
                if u:
                    ret = GRUFUser.GRUFUser(u, self, source_id=src.getUserSourceId(), isGroup=0).__of__(self)
                    return ret

        if __include_groups__ and not __force_group_id__:
            u = self._getOb('Groups')._getGroup(name)
            if u:
                ret = GRUFUser.GRUFGroup(u, self, isGroup=1, source_id='Groups').__of__(self)
                return ret
        return

    security.declareProtected(Permissions.manage_users, 'getUserById')

    def getUserById(self, id, default=_marker):
        """Return the user atom corresponding to the given id. Can return groups.
        """
        ret = self.getUser(id, __force_group_id__=1)
        if not ret:
            if default is _marker:
                return
            ret = default
        return ret

    security.declareProtected(Permissions.manage_users, 'getUserByName')

    def getUserByName(self, name, default=_marker):
        """Same as getUser() but works with a name instead of an id.
        [NOTA: Theorically, the id is a handle, while the name is the actual login name.
        But difference between a user id and a user name is unsignificant in
        all current User Folder implementations... except for GROUPS.]
        """
        usr = self.getUser(name)
        if not usr:
            name = '%s%s' % (GROUP_PREFIX, name)
            usr = self.getUserById(name, default)
        return usr

    security.declareProtected(Permissions.manage_users, 'getPureUserNames')

    def getPureUserNames(self):
        """Fetch the list of actual users from GRUFUsers.
        """
        return self.getUserNames(__include_groups__=0)

    security.declareProtected(Permissions.manage_users, 'getPureUserIds')

    def getPureUserIds(self):
        """Same as getUserIds() but without groups
        """
        return self.getUserNames(__include_groups__=0)

    security.declareProtected(Permissions.manage_users, 'getPureUsers')

    def getPureUsers(self):
        """Return a list of pure user objects.
        """
        return self.getUsers(__include_groups__=0)

    security.declareProtected(Permissions.manage_users, 'getPureUser')

    def getPureUser(self, id):
        """Return the named user object or None"""
        if not id:
            return
        return self.getUser(id, __include_groups__=0)

    security.declareProtected(Permissions.manage_users, 'getGroupNames')

    def getGroupNames(self):
        """Same as getUserNames() but without pure users.
        """
        return self.getUserNames(__include_users__=0, __groups_prefixed__=0)

    security.declareProtected(Permissions.manage_users, 'getGroupIds')

    def getGroupIds(self):
        """Same as getUserNames() but without pure users.
        """
        return self.getUserNames(__include_users__=0, __groups_prefixed__=1)

    security.declareProtected(Permissions.manage_users, 'getGroups')

    def getGroups(self):
        """Same as getUsers() but without pure users.
        """
        return self.getUsers(__include_users__=0)

    security.declareProtected(Permissions.manage_users, 'getGroup')

    def getGroup(self, name, prefixed=1):
        """Return the named user object or None"""
        if not name:
            return
        if not name.startswith(GROUP_PREFIX):
            name = '%s%s' % (GROUP_PREFIX, name)
        return self.getUser(name, __include_users__=0)

    security.declareProtected(Permissions.manage_users, 'getGroupById')

    def getGroupById(self, id, default=_marker):
        """Same as getUserById(id) but forces returning a group.
        """
        ret = self.getUser(id, __include_users__=0, __force_group_id__=1)
        if not ret:
            if default is _marker:
                return
            ret = default
        return ret

    security.declareProtected(Permissions.manage_users, 'getGroupByName')

    def getGroupByName(self, name, default=_marker):
        """Same as getUserByName(name) but forces returning a group.
        """
        ret = self.getUser(name, __include_users__=0, __force_group_id__=0)
        if not ret:
            if default is _marker:
                return
            ret = default
        return ret

    security.declareProtected(Permissions.manage_users, 'userFolderAddUser')

    def userFolderAddUser(self, name, password, roles, domains, groups=(), REQUEST=None, **kw):
        """API method for creating a new user object. Note that not all
        user folder implementations support dynamic creation of user
        objects.
        """
        return self._doAddUser(name, password, roles, domains, groups, **kw)

    userFolderAddUser = postonly(userFolderAddUser)
    security.declareProtected(Permissions.manage_users, 'userFolderEditUser')

    def userFolderEditUser(self, name, password, roles, domains, groups=None, REQUEST=None, **kw):
        """API method for changing user object attributes. Note that not
        all user folder implementations support changing of user object
        attributes.
        Arguments ARE required.
        """
        return self._doChangeUser(name, password, roles, domains, groups, **kw)

    userFolderEditUser = postonly(userFolderEditUser)
    security.declareProtected(Permissions.manage_users, 'userFolderUpdateUser')

    def userFolderUpdateUser(self, name, password=None, roles=None, domains=None, groups=None, REQUEST=None, **kw):
        """API method for changing user object attributes. Note that not
        all user folder implementations support changing of user object
        attributes.
        Arguments are optional"""
        return self._updateUser(name, password, roles, domains, groups, **kw)

    userFolderUpdateUser = postonly(userFolderUpdateUser)
    security.declareProtected(Permissions.manage_users, 'userFolderDelUsers')

    def userFolderDelUsers(self, names, REQUEST=None):
        """API method for deleting one or more user atom objects. Note that not
        all user folder implementations support deletion of user objects."""
        return self._doDelUsers(names)

    userFolderDelUsers = postonly(userFolderDelUsers)
    security.declareProtected(Permissions.manage_users, 'userFolderAddGroup')

    def userFolderAddGroup(self, name, roles, groups=(), REQUEST=None, **kw):
        """API method for creating a new group.
        """
        while name.startswith(GROUP_PREFIX):
            name = name[GROUP_PREFIX_LEN:]

        return self._doAddGroup(name, roles, groups, **kw)

    userFolderAddGroup = postonly(userFolderAddGroup)
    security.declareProtected(Permissions.manage_users, 'userFolderEditGroup')

    def userFolderEditGroup(self, name, roles, groups=None, REQUEST=None, **kw):
        """API method for changing group object attributes.
        """
        return self._doChangeGroup(name, roles=roles, groups=groups, **kw)

    userFolderEditGroup = postonly(userFolderEditGroup)
    security.declareProtected(Permissions.manage_users, 'userFolderUpdateGroup')

    def userFolderUpdateGroup(self, name, roles=None, groups=None, REQUEST=None, **kw):
        """API method for changing group object attributes.
        """
        return self._updateGroup(name, roles=roles, groups=groups, **kw)

    userFolderUpdateGroup = postonly(userFolderUpdateGroup)
    security.declareProtected(Permissions.manage_users, 'userFolderDelGroups')

    def userFolderDelGroups(self, names, REQUEST=None):
        """API method for deleting one or more group objects.
        Implem. note : All ids must be prefixed with 'group_',
        so this method ends up beeing only a filter of non-prefixed ids
        before calling userFolderDelUsers().
        """
        return self._doDelGroups(names)

    userFolderDelUsers = postonly(userFolderDelUsers)
    security.declareProtected(Permissions.manage_users, 'searchUsersByAttribute')

    def searchUsersByAttribute(self, attribute, search_term):
        """Return user ids whose 'attribute' match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying user folder:
        it may return all users, return only cached users (for LDAPUF) or return no users.
        This will return all users whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON USER FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF).
        'attribute' can be 'id' or 'name' for all UF kinds, or anything else for LDAPUF.
        """
        ret = []
        for src in self.listUserSources():
            if hasattr(src.aq_base, 'findUser'):
                Log(LOG_DEBUG, 'We use LDAPUF to find users')
                id_attr = src._uid_attr
                if attribute == 'name':
                    attr = src._login_attr
                elif attribute == 'id':
                    attr = src._uid_attr
                else:
                    attr = attribute
                Log(LOG_DEBUG, 'we use findUser', attr, search_term)
                users = src.findUser(attr, search_term, exact_match=True)
                ret.extend([ u[id_attr] for u in users ])
            else:
                search_term = search_term.lower()
                if attribute == 'name':
                    method = 'getName'
                elif attribute == 'id':
                    method = 'getId'
                else:
                    raise NotImplementedError, 'Attribute searching is only supported for LDAPUserFolder by now.'
                src_id = src.getUserSourceId()
                for u in src.getUsers():
                    if not u:
                        continue
                    u = GRUFUser.GRUFUser(u, self, source_id=src_id, isGroup=0).__of__(self)
                    s = getattr(u, method)().lower()
                    if string.find(s, search_term) != -1:
                        ret.append(u.getId())

        Log(LOG_DEBUG, "We've found them:", ret)
        return ret

    security.declareProtected(Permissions.manage_users, 'searchUsersByName')

    def searchUsersByName(self, search_term):
        """Return user ids whose name match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying user folder:
        it may return all users, return only cached users (for LDAPUF) or return no users.
        This will return all users whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON USER FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF)
        """
        return self.searchUsersByAttribute('name', search_term)

    security.declareProtected(Permissions.manage_users, 'searchUsersById')

    def searchUsersById(self, search_term):
        """Return user ids whose id match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying user folder:
        it may return all users, return only cached users (for LDAPUF) or return no users.
        This will return all users whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON USER FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF)
        """
        return self.searchUsersByAttribute('id', search_term)

    security.declareProtected(Permissions.manage_users, 'searchGroupsByAttribute')

    def searchGroupsByAttribute(self, attribute, search_term):
        """Return group ids whose 'attribute' match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying group folder:
        it may return all groups, return only cached groups (for LDAPUF) or return no groups.
        This will return all groups whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON GROUP FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF).
        'attribute' can be 'id' or 'name' for all UF kinds, or anything else for LDAPUF.
        """
        ret = []
        src = self.Groups
        if hasattr(src.aq_base, 'findGroup'):
            id_attr = src._uid_attr
            if attribute == 'name':
                attr = src._login_attr
            elif attribute == 'id':
                attr = src._uid_attr
            else:
                attr = attribute
            groups = src.findGroup(attr, search_term)
            ret.extend([ u[id_attr] for u in groups ])
        else:
            search_term = search_term.lower()
            if attribute == 'name':
                method = 'getName'
            elif attribute == 'id':
                method = 'getId'
            else:
                raise NotImplementedError, 'Attribute searching is only supported for LDAPGroupFolder by now.'
        for u in self.getGroups():
            s = getattr(u, method)().lower()
            if string.find(s, search_term) != -1:
                ret.append(u.getId())

        return ret

    security.declareProtected(Permissions.manage_users, 'searchGroupsByName')

    def searchGroupsByName(self, search_term):
        """Return group ids whose name match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying group folder:
        it may return all groups, return only cached groups (for LDAPUF) or return no groups.
        This will return all groups whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON GROUP FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF)
        """
        return self.searchGroupsByAttribute('name', search_term)

    security.declareProtected(Permissions.manage_users, 'searchGroupsById')

    def searchGroupsById(self, search_term):
        """Return group ids whose id match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying group folder:
        it may return all groups, return only cached groups (for LDAPUF) or return no groups.
        This will return all groups whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON GROUP FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF)
        """
        return self.searchGroupsByAttribute('id', search_term)

    security.declareProtected(Permissions.manage_users, 'setRolesOnUsers')

    def setRolesOnUsers(self, roles, userids, REQUEST=None):
        """Set a common set of roles for a bunch of user atoms.
        """
        for usr in userids:
            self.userSetRoles(usr, roles)

    setRolesOnUsers = postonly(setRolesOnUsers)
    security.declareProtected(Permissions.manage_users, 'getUsersOfRole')

    def getUsersOfRole(self, role, object=None):
        """Gets the user (and group) ids having the specified role...
        ...on the specified Zope object if it's not None
        ...on their own information if the object is None.
        NOTA: THIS METHOD IS VERY EXPENSIVE.
        XXX PERFORMANCES HAVE TO BE IMPROVED
        """
        ret = []
        for id in self.getUserIds():
            if role in self.getRolesOfUser(id):
                ret.append(id)

        return tuple(ret)

    security.declarePublic('getRolesOfUser')

    def getRolesOfUser(self, userid):
        """Alias for user.getRoles()
        """
        return self.getUserById(userid).getRoles()

    security.declareProtected(Permissions.manage_users, 'userFolderAddRole')

    def userFolderAddRole(self, role, REQUEST=None):
        """Add a new role. The role will be appended, in fact, in GRUF's surrounding folder.
        """
        if role in self.aq_parent.valid_roles():
            raise ValueError, "Role '%s' already exist" % (role,)
        return self.aq_parent._addRole(role)

    userFolderAddRole = postonly(userFolderAddRole)
    security.declareProtected(Permissions.manage_users, 'userFolderDelRoles')

    def userFolderDelRoles(self, roles, REQUEST=None):
        """Delete roles.
        The removed roles will be removed from the UserFolder's users and groups as well,
        so this method can be very time consuming with a large number of users.
        """
        ud_roles = self.aq_parent.userdefined_roles()
        for r in roles:
            if r not in ud_roles:
                raise ValueError, "Role '%s' is not defined on acl_users' parent folder" % (r,)

        for r in roles:
            for u in self.getUsersOfRole(r):
                self.userRemoveRole(u, r)

        return self.aq_parent._delRoles(roles, None)

    userFolderDelRoles = postonly(userFolderDelRoles)
    security.declarePublic('userFolderGetRoles')

    def userFolderGetRoles(self):
        """
        userFolderGetRoles(self,) => tuple of strings
        List the roles defined at the top of GRUF's folder.
        This includes both user-defined roles and default roles.
        """
        return tuple(self.aq_parent.valid_roles())

    security.declareProtected(Permissions.manage_users, 'setMembers')

    def setMembers(self, groupid, userids, REQUEST=None):
        """Set the members of the group
        """
        self.getGroup(groupid).setMembers(userids)

    setMembers = postonly(setMembers)
    security.declareProtected(Permissions.manage_users, 'addMember')

    def addMember(self, groupid, userid, REQUEST=None):
        """Add a member to a group
        """
        return self.getGroup(groupid).addMember(userid)

    addMember = postonly(addMember)
    security.declareProtected(Permissions.manage_users, 'removeMember')

    def removeMember(self, groupid, userid, REQUEST=None):
        """Remove a member from a group.
        """
        return self.getGroup(groupid).removeMember(userid)

    removeMember = postonly(removeMember)
    security.declareProtected(Permissions.manage_users, 'getMemberIds')

    def getMemberIds(self, groupid):
        """Return the list of member ids (groups and users) in this group
        """
        m = self.getGroup(groupid)
        if not m:
            raise ValueError, "Invalid group: '%s'" % groupid
        return self.getGroup(groupid).getMemberIds()

    security.declareProtected(Permissions.manage_users, 'getUserMemberIds')

    def getUserMemberIds(self, groupid):
        """Return the list of member ids (groups and users) in this group
        """
        return self.getGroup(groupid).getUserMemberIds()

    security.declareProtected(Permissions.manage_users, 'getGroupMemberIds')

    def getGroupMemberIds(self, groupid):
        """Return the list of member ids (groups and users) in this group
        XXX THIS MAY BE VERY EXPENSIVE !
        """
        return self.getGroup(groupid).getGroupMemberIds()

    security.declareProtected(Permissions.manage_users, 'hasMember')

    def hasMember(self, groupid, id):
        """Return true if the specified atom id is in the group.
        This is the contrary of IUserAtom.isInGroup(groupid).
        THIS CAN BE VERY EXPENSIVE
        """
        return self.getGroup(groupid).hasMember(id)

    security.declareProtected(Permissions.manage_users, 'userSetRoles')

    def userSetRoles(self, id, roles, REQUEST=None):
        """Change the roles of a user atom.
        """
        self._updateUser(id, roles=roles)

    userSetRoles = postonly(userSetRoles)
    security.declareProtected(Permissions.manage_users, 'userAddRole')

    def userAddRole(self, id, role, REQUEST=None):
        """Append a role for a user atom
        """
        roles = list(self.getUser(id).getRoles())
        if role not in roles:
            roles.append(role)
            self._updateUser(id, roles=roles)

    userAddRole = postonly(userAddRole)
    security.declareProtected(Permissions.manage_users, 'userRemoveRole')

    def userRemoveRole(self, id, role, REQUEST=None):
        """Remove the role of a user atom. Will NOT complain if role doesn't exist
        """
        roles = list(self.getRolesOfUser(id))
        if role in roles:
            roles.remove(role)
            self._updateUser(id, roles=roles)

    userRemoveRole = postonly(userRemoveRole)
    security.declareProtected(Permissions.manage_users, 'userSetPassword')

    def userSetPassword(self, id, newPassword, REQUEST=None):
        """Set the password of a user
        """
        u = self.getPureUser(id)
        if not u:
            raise ValueError, "Invalid pure user id: '%s'" % (id,)
        self._updateUser(u.getId(), password=newPassword)

    userSetPassword = postonly(userSetPassword)
    security.declareProtected(Permissions.manage_users, 'userGetDomains')

    def userGetDomains(self, id):
        """get domains for a user
        """
        usr = self.getPureUser(id)
        return tuple(usr.getDomains())

    security.declareProtected(Permissions.manage_users, 'userSetDomains')

    def userSetDomains(self, id, domains, REQUEST=None):
        """Set domains for a user
        """
        usr = self.getPureUser(id)
        self._updateUser(usr.getId(), domains=domains)

    userSetDomains = postonly(userSetDomains)
    security.declareProtected(Permissions.manage_users, 'userAddDomain')

    def userAddDomain(self, id, domain, REQUEST=None):
        """Append a domain to a user
        """
        usr = self.getPureUser(id)
        domains = list(usr.getDomains())
        if domain not in domains:
            roles.append(domain)
            self._updateUser(usr.getId(), domains=domains)

    userAddDomain = postonly(userAddDomain)
    security.declareProtected(Permissions.manage_users, 'userRemoveDomain')

    def userRemoveDomain(self, id, domain, REQUEST=None):
        """Remove a domain from a user
        """
        usr = self.getPureUser(id)
        domains = list(usr.getDomains())
        if domain not in domains:
            raise ValueError, "User '%s' doesn't have domain '%s'" % (id, domain)
        while domain in domains:
            roles.remove(domain)

        self._updateUser(usr.getId(), domains=domains)

    userRemoveDomain = postonly(userRemoveDomain)
    security.declareProtected(Permissions.manage_users, 'userSetGroups')

    def userSetGroups(self, id, groupnames, REQUEST=None):
        """Set the groups of a user
        """
        self._updateUser(id, groups=groupnames)

    userSetGroups = postonly(userSetGroups)
    security.declareProtected(Permissions.manage_users, 'userAddGroup')

    def userAddGroup(self, id, groupname, REQUEST=None):
        """add a group to a user atom
        """
        groups = list(self.getUserById(id).getGroups())
        if groupname not in groups:
            groups.append(groupname)
            self._updateUser(id, groups=groups)

    userAddGroup = postonly(userAddGroup)
    security.declareProtected(Permissions.manage_users, 'userRemoveGroup')

    def userRemoveGroup(self, id, groupname, REQUEST=None):
        """remove a group from a user atom.
        """
        groups = list(self.getUserById(id).getGroupNames())
        if groupname.startswith(GROUP_PREFIX):
            groupname = groupname[GROUP_PREFIX_LEN:]
        if groupname in groups:
            groups.remove(groupname)
            self._updateUser(id, groups=groups)

    userRemoveGroup = postonly(userRemoveGroup)

    def __init__(self):
        """
        __init__(self) -> initialization method
        We define it to prevend calling ancestor's __init__ methods.
        """
        pass

    security.declarePrivate('_post_init')

    def _post_init(self):
        """
        _post_init(self) => meant to be called when the
                            object is in the Zope tree
        """
        uf = GRUFFolder.GRUFUsers()
        gf = GRUFFolder.GRUFGroups()
        self._setObject('Users', uf)
        self._setObject('Groups', gf)
        self.id = 'acl_users'

    def manage_beforeDelete(self, item, container):
        """
        Special overloading for __allow_groups__ attribute
        """
        if item is self:
            try:
                del container.__allow_groups__
            except:
                pass

    def manage_afterAdd(self, item, container):
        """Same
        """
        if item is self:
            container.__allow_groups__ = aq_base(self)

    security.declarePublic('getGroupPrefix')

    def getGroupPrefix(self):
        """ group prefix """
        return GROUP_PREFIX

    security.declarePrivate('getGRUFPhysicalRoot')

    def getGRUFPhysicalRoot(self):
        return self.getPhysicalRoot()

    security.declareProtected(Permissions.view, 'getGRUFId')

    def getGRUFId(self):
        """
        Alias to self.getId()
        """
        return self.getId()

    security.declareProtected(Permissions.manage_users, 'getUnwrappedUser')

    def getUnwrappedUser(self, name):
        """
        getUnwrappedUser(self, name) => user object or None

        This method is used to get a User object directly from the User's
        folder acl_users, without wrapping it with group information.

        This is useful for UserFolders that define additional User classes,
        when you want to call specific methods on these user objects.

        For example, LDAPUserFolder defines a 'getProperty' method that's
        not inherited from the standard User object. You can, then, use
        the getUnwrappedUser() to get the matching user and call this
        method.
        """
        src_id = self.getUser(name).getUserSourceId()
        return self.getUserSource(src_id).getUser(name)

    security.declareProtected(Permissions.manage_users, 'getUnwrappedGroup')

    def getUnwrappedGroup(self, name):
        """
        getUnwrappedGroup(self, name) => user object or None

        Same as getUnwrappedUser but for groups.
        """
        return self.Groups.acl_users.getUser(name)

    security.declarePrivate('authenticate')

    def authenticate(self, name, password, request):
        """
        Pass the request along to the underlying user-related UserFolder
        object
        THIS METHOD RETURNS A USER OBJECT OR NONE, as specified in the code
        in AccessControl/User.py.
        We also check for inituser in there.
        """
        emergency = self._emergency_user
        if emergency and name == emergency.getUserName():
            if emergency.authenticate(password, request):
                return emergency
            else:
                return
        for src in self.listUserSources():
            u = src.authenticate(name, password, request)
            if u:
                return GRUFUser.GRUFUser(u, self, isGroup=0, source_id=src.getUserSourceId()).__of__(self)

        return

    security.declarePrivate('_doAddUser')

    def _doAddUser(self, name, password, roles, domains, groups=(), **kw):
        """
        Create a new user. This should be implemented by subclasses to
        do the actual adding of a user. The 'password' will be the
        original input password, unencrypted. The implementation of this
        method is responsible for performing any needed encryption.
        """
        prefix = GROUP_PREFIX
        roles = list(roles)
        gruf_groups = self.getGroupIds()
        for group in groups:
            if not group.startswith(prefix):
                group = '%s%s' % (prefix, group)
            if group not in gruf_groups:
                raise ValueError, "Invalid group: '%s'" % (group,)
            roles.append(group)

        self._v_batch_users = []
        return self.getDefaultUserSource()._doAddUser(name, password, roles, domains, **kw)

    security.declarePrivate('_doChangeUser')

    def _doChangeUser(self, name, password, roles, domains, groups=None, **kw):
        """
        Modify an existing user. This should be implemented by subclasses
        to make the actual changes to a user. The 'password' will be the
        original input password, unencrypted. The implementation of this
        method is responsible for performing any needed encryption.

        A None password should not change it (well, we hope so)
        """
        usr = self.getUser(name)
        if usr is None:
            raise ValueError, "Invalid user: '%s'" % (name,)
        id = usr.getRealId()
        if groups is None:
            groups = usr.getGroups()
        roles = list(roles)
        groups = list(groups)
        cur_groups = self.getGroups()
        given_roles = tuple(usr.getRoles()) + tuple(roles)
        for group in groups:
            if not group.startswith(GROUP_PREFIX):
                group = '%s%s' % (GROUP_PREFIX, group)
            if group not in cur_groups and group not in given_roles:
                roles.append(group)

        self._v_batch_users = []
        src = usr.getUserSourceId()
        Log(LOG_NOTICE, name, 'Source:', src)
        ret = self.getUserSource(src)._doChangeUser(id, password, roles, domains, **kw)
        usr.clearCachedGroupsAndRoles()
        authenticated = getSecurityManager().getUser()
        if id == authenticated.getId() and hasattr(authenticated, 'clearCachedGroupsAndRoles'):
            authenticated.clearCachedGroupsAndRoles(self.getUserSource(src).getUser(id))
        return ret

    security.declarePrivate('_updateUser')

    def _updateUser(self, id, password=None, roles=None, domains=None, groups=None):
        """
        _updateUser(self, id, password = None, roles = None, domains = None, groups = None)

        This one should work for users AND groups.

        Front-end to _doChangeUser, but with a better default value support.
        We guarantee that None values will let the underlying UF keep the original ones.
        This is not true for the password: some buggy UF implementation may not
        handle None password correctly :-(
        """
        usr = self.getUser(id)
        if roles is None:
            roles = usr._original_roles
            roles = filter(lambda x: not x.startswith(GROUP_PREFIX), roles)
            roles = filter(lambda x: x not in ('Anonymous', 'Authenticated', 'Shared', ''), roles)
        else:
            roles = filter(lambda x: x not in ('Anonymous', 'Authenticated', 'Shared', ''), roles)
            vr = self.userFolderGetRoles()
            for r in roles:
                if r not in vr:
                    raise ValueError, "Invalid or inexistant role: '%s'." % (r,)

        if domains is None:
            domains = usr._original_domains
        if groups is None:
            groups = usr.getGroups(no_recurse=1)
        glist = self.getGroupNames()
        glist.extend(map(lambda x: '%s%s' % (GROUP_PREFIX, x), glist))
        for g in groups:
            if g not in glist:
                raise ValueError, "Invalid group: '%s'" % (g,)

        self._v_batch_users = []
        return self._doChangeUser(id, password, roles, domains, groups)

    security.declarePrivate('_doDelUsers')

    def _doDelUsers(self, names):
        """
        Delete one or more users. This should be implemented by subclasses
        to do the actual deleting of users.
        This won't delete groups !
        """
        sources = {}
        for name in names:
            usr = self.getUser(name, __include_groups__=0)
            if not usr:
                continue
            src = usr.getUserSourceId()
            if not sources.has_key(src):
                sources[src] = []
            sources[src].append(name)

        for (src, names) in sources.items():
            self.getUserSource(src)._doDelUsers(names)

        self._v_batch_users = []

    security.declarePrivate('_doAddGroup')

    def _doAddGroup(self, name, roles, groups=(), **kw):
        """
        Create a new group. Password will be randomly created, and domain will be None.
        Supports nested groups.
        """
        domains = ()
        password = ''
        if roles is None:
            roles = []
        if groups is None:
            groups = []
        for x in range(0, 10):
            password = '%s%s' % (password, random.choice(string.lowercase))

        roles = list(roles)
        prefix = GROUP_PREFIX
        gruf_groups = self.getGroupIds()
        for group in groups:
            if not group.startswith(prefix):
                group = '%s%s' % (prefix, group)
            if group == '%s%s' % (prefix, name):
                raise ValueError, "Infinite recursion for group '%s'." % (group,)
            if group not in gruf_groups:
                raise ValueError, "Invalid group: '%s' (defined groups are %s)" % (group, gruf_groups)
            roles.append(group)

        self._v_batch_users = []
        return self.Groups.acl_users._doAddUser(name, password, roles, domains, **kw)

    security.declarePrivate('_doChangeGroup')

    def _doChangeGroup(self, name, roles, groups=None, **kw):
        """Modify an existing group."""
        if name.startswith(self.getGroupPrefix()):
            name = name[GROUP_PREFIX_LEN:]
        grp = self.getGroup(name, prefixed=0)
        if grp is None:
            raise ValueError, "Invalid group: '%s'" % (name,)
        if not groups:
            groups = grp.getGroups()
        roles = list(roles or [])
        groups = list(groups or [])
        cur_groups = self.getGroups()
        given_roles = tuple(grp.getRoles()) + tuple(roles)
        for group in groups:
            if not group.startswith(GROUP_PREFIX):
                group = '%s%s' % (GROUP_PREFIX, group)
            if group == '%s%s' % (GROUP_PREFIX, grp.id):
                raise ValueError, "Cannot affect group '%s' to itself!" % (name,)
            new_grp = self.getGroup(group)
            if not new_grp:
                raise ValueError, "Invalid or inexistant group: '%s'" % (group,)
            if '%s%s' % (GROUP_PREFIX, grp.id) in new_grp.getGroups():
                raise ValueError, "Cannot affect %s to group '%s' as it would lead to circular references." % (group, name)
            if group not in cur_groups and group not in given_roles:
                roles.append(group)

        self._v_batch_users = []
        domains = ''
        password = ''
        for x in range(0, 10):
            password = '%s%s' % (password, random.choice(string.lowercase))

        return self.Groups.acl_users._doChangeUser(name, password, roles, domains, **kw)

    security.declarePrivate('_updateGroup')

    def _updateGroup(self, name, roles=None, groups=None):
        """
        _updateGroup(self, name, roles = None, groups = None)

        Front-end to _doChangeUser, but with a better default value support.
        We guarantee that None values will let the underlying UF keep the original ones.
        This is not true for the password: some buggy UF implementation may not
        handle None password correctly but we do not care for Groups.

        group name can be prefixed or not
        """
        if name.startswith(self.getGroupPrefix()):
            name = name[GROUP_PREFIX_LEN:]
        usr = self.getGroup(name, prefixed=0)
        if roles is None:
            roles = usr._original_roles
            roles = filter(lambda x: not x.startswith(GROUP_PREFIX), roles)
            roles = filter(lambda x: x not in ('Anonymous', 'Authenticated', 'Shared'), roles)
        if groups is None:
            groups = usr.getGroups(no_recurse=1)
        self._v_batch_users = []
        return self._doChangeGroup(name, roles, groups)

    security.declarePrivate('_doDelGroup')

    def _doDelGroup(self, name):
        """Delete one user."""
        if name.startswith(self.getGroupPrefix()):
            name = name[GROUP_PREFIX_LEN:]
        self._v_batch_users = []
        return self.Groups.acl_users._doDelUsers([name])

    security.declarePrivate('_doDelGroups')

    def _doDelGroups(self, names):
        """Delete one or more users."""
        for group in names:
            if not self.getGroupByName(group, None):
                continue
            self._doDelGroup(group)

        return

    security.declarePublic('getGRUFVersion')

    def getGRUFVersion(self):
        """
        getGRUFVersion(self,) => Return human-readable GRUF version as a string.
        """
        rev_date = '$Date: 2007-04-01 17:13:44 +0200 (dim, 01 avr 2007) $'[7:-2]
        return '%s / Revised %s' % (version__, rev_date)

    reset_entry = '__None__'
    security.declareProtected(Permissions.manage_users, 'changeUser')

    def changeUser(self, user, groups=[], roles=[], REQUEST={}):
        """
        changeUser(self, user, groups = [], roles = [], REQUEST = {}, ) => used in ZMI
        """
        obj = self.getUser(user)
        if obj.isGroup():
            self._updateGroup(name=user, groups=groups, roles=roles)
        else:
            self._updateUser(id=user, groups=groups, roles=roles)
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/' + obj.getId() + '/manage_workspace?FORCE_USER=1')

    changeUser = postonly(changeUser)
    security.declareProtected(Permissions.manage_users, 'deleteUser')

    def deleteUser(self, user, REQUEST={}):
        """
        deleteUser(self, user, REQUEST = {}, ) => used in ZMI
        """
        pass

    deleteUser = postonly(deleteUser)
    security.declareProtected(Permissions.manage_users, 'changeOrCreateUsers')

    def changeOrCreateUsers(self, users=[], groups=[], roles=[], new_users=[], default_password='', REQUEST={}):
        """
        changeOrCreateUsers => affect roles & groups to users and/or create new users

        All parameters are strings or lists (NOT tuples !).
        NO CHECKING IS DONE. This is an utility method, it's not part of the official API.
        """
        del_roles = 0
        del_groups = 0
        if self.reset_entry in roles:
            roles.remove(self.reset_entry)
            del_roles = 1
        if self.reset_entry in groups:
            groups.remove(self.reset_entry)
            del_groups = 1
        if not roles and not del_roles:
            roles = None
            add_roles = []
        else:
            add_roles = roles
        if not groups and not del_groups:
            groups = None
            add_groups = []
        else:
            add_groups = groups
        passwords_list = []
        for new in new_users:
            name = string.strip(new)
            if not name:
                continue
            if name in map(lambda x: x.getId(), self.getUsers()):
                continue
            if default_password:
                password = default_password
            password = ''
            for x in range(0, 8):
                password = '%s%s' % (password, random.choice('ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'))

            self._doAddUser(name, password, add_roles, (), add_groups)
            passwords_list.append({'name': name, 'password': password})

        for user in users:
            self._updateUser(id=user, groups=groups, roles=roles)

        if REQUEST.has_key('RESPONSE'):
            if not passwords_list:
                return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_users')
            else:
                REQUEST.set('USER_PASSWORDS', passwords_list)
                return self.manage_newusers(None, self)
        return passwords_list

    changeOrCreateUsers = postonly(changeOrCreateUsers)
    security.declareProtected(Permissions.manage_users, 'deleteUsers')

    def deleteUsers(self, users=[], REQUEST={}):
        """
        deleteUsers => explicit

        All parameters are strings. NO CHECKING IS DONE. This is an utility method !
        """
        self._doDelUsers(users)
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_users')

    deleteUsers = postonly(deleteUsers)
    security.declareProtected(Permissions.manage_users, 'changeOrCreateGroups')

    def changeOrCreateGroups(self, groups=[], roles=[], nested_groups=[], new_groups=[], REQUEST={}):
        """
        changeOrCreateGroups => affect roles to groups and/or create new groups

        All parameters are strings. NO CHECKING IS DONE. This is an utility method !
        """
        del_roles = 0
        del_groups = 0
        if self.reset_entry in roles:
            roles.remove(self.reset_entry)
            del_roles = 1
        if self.reset_entry in nested_groups:
            nested_groups.remove(self.reset_entry)
            del_groups = 1
        if not roles and not del_roles:
            roles = None
            add_roles = []
        else:
            add_roles = roles
        if not nested_groups and not del_groups:
            nested_groups = None
            add_groups = []
        else:
            add_groups = nested_groups
        for new in new_groups:
            name = string.strip(new)
            if not name:
                continue
            self._doAddGroup(name, roles, groups=add_groups)

        for group in groups:
            self._updateGroup(group, roles=roles, groups=nested_groups)

        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_groups')
        return

    changeOrCreateGroups = postonly(changeOrCreateGroups)
    security.declareProtected(Permissions.manage_users, 'deleteGroups')

    def deleteGroups(self, groups=[], REQUEST={}):
        """
        deleteGroups => explicit

        All parameters are strings. NO CHECKING IS DONE. This is an utility method !
        """
        for group in groups:
            self._doDelGroup(group)

        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_groups')

    deleteGroups = postonly(deleteGroups)
    security.declarePublic('acquireLocalRoles')

    def acquireLocalRoles(self, folder, status, REQUEST=None):
        """
        Enable or disable local role acquisition on the specified folder.
        If status is true, it will enable, else it will disable.
        Note that the user _must_ have the change_permissions permission on the
        folder to allow changes on it.
        If you want to use this code from a product, please use _acquireLocalRoles()
        instead: this private method won't check security on the destination folder.
        It's usually a bad idea to use _acquireLocalRoles() directly in your product,
        but, well, after all, you do what you want ! :^)
        """
        if not getSecurityManager().checkPermission(Permissions.change_permissions, folder):
            raise Unauthorized(name='acquireLocalRoles')
        return self._acquireLocalRoles(folder, status)

    acquireLocalRoles = postonly(acquireLocalRoles)

    def _acquireLocalRoles(self, folder, status):
        """Same as _acquireLocalRoles() but won't perform security check on the folder.
        """
        if not status:
            folder.__ac_local_roles_block__ = 1
        elif getattr(folder, '__ac_local_roles_block__', None):
            folder.__ac_local_roles_block__ = None
        return

    security.declarePublic('isLocalRoleAcquired')

    def isLocalRoleAcquired(self, folder):
        """Return true if the specified folder allows local role acquisition.
        """
        if getattr(folder, '__ac_local_roles_block__', None):
            return 0
        return 1

    security.declarePublic('getLocalRolesForDisplay')

    def getLocalRolesForDisplay(self, object):
        """This is used for plone's local roles display
        This method returns a tuple (massagedUsername, roles, userType, actualUserName).
        This method is protected by the 'Manage properties' permission. We may
        change that if it's too permissive..."""
        if not getSecurityManager().checkPermission(Permissions.manage_properties, object):
            raise Unauthorized(name='getLocalRolesForDisplay')
        return self._getLocalRolesForDisplay(object)

    def _getLocalRolesForDisplay(self, object):
        """This is used for plone's local roles display
        This method returns a tuple (massagedUsername, roles, userType, actualUserName)"""
        result = []
        local_roles = object.get_local_roles()
        prefix = self.getGroupPrefix()
        for one_user in local_roles:
            massagedUsername = username = one_user[0]
            roles = one_user[1]
            userType = 'user'
            if prefix:
                if self.getGroupById(username) is not None:
                    massagedUsername = username[len(prefix):]
                    userType = 'group'
            else:
                userType = 'unknown'
            result.append((massagedUsername, roles, userType, username))

        return tuple(result)

    security.declarePublic('getAllLocalRoles')

    def getAllLocalRoles(self, object):
        """getAllLocalRoles(self, object): return a dictionnary {useratom_id: roles} of local
        roles defined AND herited at a certain point. This will handle lr-blocking
        as well.
        """
        if not getSecurityManager().checkPermission(Permissions.change_permissions, object):
            raise Unauthorized(name='getAllLocalRoles')
        return self._getAllLocalRoles(object)

    def _getAllLocalRoles(self, object):
        """getAllLocalRoles(self, object): return a dictionnary {useratom_id: roles} of local
        roles defined AND herited at a certain point. This will handle lr-blocking
        as well.
        """
        merged = {}
        object = getattr(object, 'aq_inner', object)
        while 1:
            if hasattr(object, '__ac_local_roles__'):
                dict = object.__ac_local_roles__ or {}
                if callable(dict):
                    dict = dict()
                for (k, v) in dict.items():
                    if not merged.has_key(k):
                        merged[k] = {}
                    for role in v:
                        merged[k][role] = 1

            if not self.isLocalRoleAcquired(object):
                break
            if hasattr(object, 'aq_parent'):
                object = object.aq_parent
                object = getattr(object, 'aq_inner', object)
                continue
            if hasattr(object, 'im_self'):
                object = object.im_self
                object = getattr(object, 'aq_inner', object)
                continue
            break

        for (key, value) in merged.items():
            merged[key] = value.keys()

        return merged

    security.declarePublic('getPloneSecurityMatrix')

    def getPloneSecurityMatrix(self, object):
        """getPloneSecurityMatrix(self, object): return a list of dicts of the current object
        and all its parents. The list is sorted with portal object first.
        Each dict has the following structure:
        {
          depth: (0 for portal root, 1 for 1st-level folders and so on),
          id:
          title:
          icon:
          absolute_url:
          security_permission: true if current user can change security on this object
          state: (workflow state)
          acquired_local_roles: 0 if local role blocking is enabled for this folder
          roles: {
            'role1': {
              'all_local_roles': [r1, r2, r3, ] (all defined local roles, including parent ones)
              'defined_local_roles': [r3, ] (local-defined only local roles)
              'permissions': ['Access contents information', 'Modify portal content', ] (only a subset)
              'same_permissions': true if same permissions as the parent
              'same_all_local_roles': true if all_local_roles is the same as the parent
              'same_defined_local_roles': true if defined_local_roles is the same as the parent
              },
            'role2': {...},
            },
        }
        """
        if not getSecurityManager().checkPermission(Permissions.access_contents_information, object):
            raise Unauthorized(name='getPloneSecurityMatrix')
        mt = self.portal_membership
        all_roles = [
         'Anonymous'] + mt.getPortalRoles()
        all_objects = []
        cur_object = object
        while 1:
            if not getSecurityManager().checkPermission(Permissions.access_contents_information, cur_object):
                raise Unauthorized(name='getPloneSecurityMatrix')
            all_objects.append(cur_object)
            if cur_object.meta_type == 'Plone Site':
                break
            cur_object = object.aq_parent

        all_objects.reverse()
        ret = []
        previous = None
        count = 0
        for obj in all_objects:
            current = {'depth': count, 'id': obj.getId(), 'title': obj.Title(), 'icon': obj.getIcon(), 'absolute_url': obj.absolute_url(), 'security_permission': getSecurityManager().checkPermission(Permissions.change_permissions, obj), 'acquired_local_roles': self.isLocalRoleAcquired(obj), 'roles': {}, 'state': 'XXX TODO XXX'}
            count += 1
            all_local_roles = {}
            local_roles = self._getAllLocalRoles(obj)
            for (user, roles) in self._getAllLocalRoles(obj).items():
                for role in roles:
                    if not all_local_roles.has_key(role):
                        all_local_roles[role] = {}
                    all_local_roles[role][user] = 1

            defined_local_roles = {}
            if hasattr(obj.aq_base, 'get_local_roles'):
                for (user, roles) in obj.get_local_roles():
                    for role in roles:
                        if not defined_local_roles.has_key(role):
                            defined_local_roles[role] = {}
                        defined_local_roles[role][user] = 1

            for role in all_roles:
                all = all_local_roles.get(role, {}).keys()
                defined = defined_local_roles.get(role, {}).keys()
                all.sort()
                defined.sort()
                same_all_local_roles = 0
                same_defined_local_roles = 0
                if previous:
                    if previous['roles'][role]['all_local_roles'] == all:
                        same_all_local_roles = 1
                    if previous['roles'][role]['defined_local_roles'] == defined:
                        same_defined_local_roles = 1
                current['roles'][role] = {'all_local_roles': all, 'defined_local_roles': defined, 'same_all_local_roles': same_all_local_roles, 'same_defined_local_roles': same_defined_local_roles, 'permissions': []}

            ret.append(current)
            previous = current

        return ret

    security.declareProtected(Permissions.manage_users, 'computeSecuritySettings')

    def computeSecuritySettings(self, folders, actors, permissions, cache={}):
        """
        computeSecuritySettings(self, folders, actors, permissions, cache = {}) => return a structure that is suitable for security audit Page Template.

        - folders is the structure returned by getSiteTree()
        - actors is the structure returned by listUsersAndRoles()
        - permissions is ((id: permission), (id: permission), ...)
        - cache is passed along requests to make computing faster
        """
        usr_cache = {}
        for (id, depth, path) in folders:
            folder = self.unrestrictedTraverse(path)
            for (kind, actor, display, handle, html) in actors:
                if kind in ('user', 'group'):
                    if not cache.has_key(path):
                        cache[path] = {(kind, actor): {}}
                    elif not cache[path].has_key((kind, actor)):
                        cache[path][(kind, actor)] = {}
                    else:
                        cache[path][(kind, actor)] = {}
                    perm_keys = []
                    usr = usr_cache.get(actor)
                    if not usr:
                        usr = self.getUser(actor)
                        usr_cache[actor] = usr
                    roles = usr.getRolesInContext(folder)
                    for role in roles:
                        for perm_key in self.computeSetting(path, folder, role, permissions, cache).keys():
                            cache[path][(kind, actor)][perm_key] = 1

                else:
                    self.computeSetting(path, folder, actor, permissions, cache)

        return cache

    security.declareProtected(Permissions.manage_users, 'computeSetting')

    def computeSetting(self, path, folder, actor, permissions, cache):
        """
        computeSetting(......) => used by computeSecuritySettings to populate the cache for ROLES
        """
        kind = 'role'
        if cache.get(path, {}).get((kind, actor), None) is not None:
            return cache[path][(kind, actor)]
        if not cache.has_key(path):
            cache[path] = {(kind, actor): {}}
        elif not cache[path].has_key((kind, actor)):
            cache[path][(kind, actor)] = {}
        ps = folder.permission_settings()
        for (perm_key, permission) in permissions:
            can = 0
            acquired = 0
            for p in ps:
                if p['name'] == permission:
                    acquired = not not p['acquire']

            if acquired:
                parent = folder.aq_parent.getPhysicalPath()
                perms = self.computeSetting(parent, self.unrestrictedTraverse(parent), actor, permissions, cache)
                can = perms.get(perm_key, None)
            for p in folder.rolesOfPermission(permission):
                if p['name'] == 'Anonymous':
                    if p['selected']:
                        can = 1
                        break
                if p['name'] == actor:
                    if p['selected']:
                        can = 1
                        break

            if can:
                cache[path][(kind, actor)][perm_key] = 1

        return cache[path][(kind, actor)]

    security.declarePrivate('_getNextHandle')

    def _getNextHandle(self, index):
        """
        _getNextHandle(self, index) => utility function to
        get an unique handle for each legend item.
        """
        return '%02d' % index

    security.declareProtected(Permissions.manage_users, 'listUsersAndRoles')

    def listUsersAndRoles(self):
        """
        listUsersAndRoles(self,) => list of tuples

        This method is used by the Security Audit page.
        XXX HAS TO BE OPTIMIZED
        """
        request = self.REQUEST
        display_roles = request.get('display_roles', 0)
        display_groups = request.get('display_groups', 0)
        display_users = request.get('display_users', 0)
        role_index = 0
        user_index = 0
        group_index = 0
        ret = []
        if display_roles:
            for r in self.aq_parent.valid_roles():
                handle = 'R%02d' % role_index
                role_index += 1
                ret.append(('role', r, r, handle, r))

        if display_users:
            for u in map(lambda x: x.getId(), self.getPureUsers()):
                obj = self.getUser(u)
                html = obj.asHTML()
                handle = 'U%02d' % user_index
                user_index += 1
                ret.append(('user', u, u, handle, html))

        if display_groups:
            for u in self.getGroupNames():
                obj = self.getUser(u)
                handle = 'G%02d' % group_index
                html = obj.asHTML()
                group_index += 1
                ret.append(('group', u, obj.getUserNameWithoutGroupPrefix(), handle, html))

        return ret

    security.declareProtected(Permissions.manage_users, 'getSiteTree')

    def getSiteTree(self, obj=None, depth=0):
        """
        getSiteTree(self, obj=None, depth=0) => special structure

        This is used by the security audit page
        """
        ret = []
        if not obj:
            if depth == 0:
                obj = self.aq_parent
            else:
                return ret
        ret.append([obj.getId(), depth, string.join(obj.getPhysicalPath(), '/')])
        for sub in obj.objectValues():
            try:
                if sub.getId() in ('acl_users', ):
                    continue
                if sub.getId()[:len('portal_')] == 'portal_':
                    continue
                if sub.isPrincipiaFolderish:
                    ret.extend(self.getSiteTree(sub, depth + 1))
            except:
                pass

        return ret

    security.declareProtected(Permissions.manage_users, 'listAuditPermissions')

    def listAuditPermissions(self):
        """
        listAuditPermissions(self,) => return a list of eligible permissions
        """
        ps = self.permission_settings()
        return map(lambda p: p['name'], ps)

    security.declareProtected(Permissions.manage_users, 'getDefaultPermissions')

    def getDefaultPermissions(self):
        """
        getDefaultPermissions(self,) => return default R & W permissions for security audit.
        """
        hasPlone = 0
        p = self.aq_parent
        if p.meta_type == 'CMF Site':
            hasPlone = 1
        else:
            for obj in p.objectValues():
                if obj.meta_type == 'CMF Site':
                    hasPlone = 1
                    break

            if hasPlone:
                return {'R': 'View', 'W': 'Modify portal content'}
            else:
                return {'R': 'View', 'W': 'Change Images and Files'}

    security.declarePrivate('getTreeInfo')

    def getTreeInfo(self, usr, dict={}):
        """utility method"""
        name = usr.getUserName()
        if dict.has_key(name):
            return
        dict[name] = {}
        noprefix = usr.getUserNameWithoutGroupPrefix()
        is_group = usr.isGroup()
        if usr.isGroup():
            icon = string.join(self.getPhysicalPath(), '/') + '/img_group'
        else:
            icon = ' img_user'
        belongs_to = []
        for grp in usr.getGroups(no_recurse=1):
            belongs_to.append(grp)
            self.getTreeInfo(self.getGroup(grp))

        dict[name] = {'name': noprefix, 'is_group': is_group, 'icon': icon, 'belongs_to': belongs_to}
        return dict

    security.declarePrivate('tpValues')

    def tpValues(self):
        if self._v_no_tree and self._v_cache_no_tree > time.time():
            return []
        return []
        ngroups = len(self.getGroupNames())
        if ngroups > MAX_TREE_USERS_AND_GROUPS:
            self._v_no_tree = 1
            self._v_cache_no_tree = time.time() + TREE_CACHE_TIME
            return []
        nusers = len(self.getUsers())
        if ngroups + nusers > MAX_TREE_USERS_AND_GROUPS:
            meth_list = self.getGroups
        else:
            meth_list = self.getUsers
        self._v_no_tree = 0
        tree_dict = {}
        top_level_names = []
        top_level = []
        for usr in meth_list():
            self.getTreeInfo(usr, tree_dict)
            if not usr.getGroups(no_recurse=1):
                top_level_names.append(usr.getUserName())

        for id in top_level_names:
            top_level.append(treeWrapper(id, tree_dict))

        top_level.sort(lambda x, y: cmp(x.sortId(), y.sortId()))
        return top_level

    def tpId(self):
        return self.getId()

    def manage_workspace(self, REQUEST):
        """
        manage_workspace(self, REQUEST) => Overrided to allow direct user or group traversal
        via the left tree view.
        """
        path = string.split(REQUEST.PATH_INFO, '/')[:-1]
        userid = path[(-1)]
        if userid != 'acl_users':
            usr = self.getUserById(userid)
            if usr:
                REQUEST.set('username', userid)
                REQUEST.set('MANAGE_TABS_NO_BANNER', '1')
                return self.restrictedTraverse('manage_user')()
        return self.restrictedTraverse('manage_overview')()

    _v_no_tree = 0
    _v_cache_no_tree = 0
    _v_cache_tree = (0, [])

    def __bobo_traverse__(self, request, name):
        """
        Looks for the name of a user or a group.
        This applies only if users list is not huge.
        """
        if hasattr(self.aq_base, name):
            return getattr(self, name)
        if name.startswith('_'):
            pass
        elif name.startswith('manage_'):
            pass
        elif name in INVALID_USER_NAMES:
            pass
        else:
            if self._v_cache_tree[0] < time.time():
                un = map(lambda x: x.getId(), self.getUsers())
                self._v_cache_tree = (time.time() + TREE_CACHE_TIME, un)
            else:
                un = self._v_cache_tree[1]
            if name in un:
                self._v_no_tree = 0
                return self
            if request.get('FORCE_USER'):
                self._v_no_tree = 0
                return self
        return getattr(self, name)

    _v_batch_users = []
    security.declareProtected(Permissions.view_management_screens, 'listUsersBatches')

    def listUsersBatches(self):
        """
        listUsersBatches(self,) => return a list of (start, end) tuples.
        Return None if batching is not necessary
        """
        un = map(lambda x: x.getId(), self.getPureUsers())
        if len(un) <= MAX_USERS_PER_PAGE:
            return
        un.sort()
        ret = []
        idx = 0
        l_un = len(un)
        nbatches = int(math.ceil(l_un / float(MAX_USERS_PER_PAGE)))
        for idx in range(0, nbatches):
            first = idx * MAX_USERS_PER_PAGE
            last = first + MAX_USERS_PER_PAGE - 1
            if last >= l_un:
                last = l_un - 1
            ret.append((first, last, un[first], un[last]))

        self._v_batch_users = un
        return ret

    security.declareProtected(Permissions.view_management_screens, 'listUsersBatchTable')

    def listUsersBatchTable(self):
        """
        listUsersBatchTable(self,) => Same a mgt screens but divided into sublists to
        present them into 5 columns.
        XXX have to merge this w/getUsersBatch to make it in one single pass
        """
        ret = []
        idx = 0
        current = []
        for rec in self.listUsersBatches() or []:
            if not idx % 5:
                if current:
                    ret.append(current)
                current = []
            current.append(rec)
            idx += 1

        if current:
            ret.append(current)
        return ret

    security.declareProtected(Permissions.view_management_screens, 'getUsersBatch')

    def getUsersBatch(self, start):
        """
        getUsersBatch(self, start) => user list
        """
        if not self._v_batch_users:
            un = map(lambda x: x.getId(), self.getPureUsers())
            self._v_batch_users = un
        end = start + MAX_USERS_PER_PAGE
        ids = self._v_batch_users[start:end]
        ret = []
        for id in ids:
            usr = self.getUser(id)
            if usr:
                ret.append(usr)

        return ret

    img_up_arrow = ImageFile.ImageFile('www/up_arrow.gif', globals())
    img_down_arrow = ImageFile.ImageFile('www/down_arrow.gif', globals())
    img_up_arrow_grey = ImageFile.ImageFile('www/up_arrow_grey.gif', globals())
    img_down_arrow_grey = ImageFile.ImageFile('www/down_arrow_grey.gif', globals())
    security.declareProtected(Permissions.manage_users, 'toggleSource')

    def toggleSource(self, src_id, REQUEST={}):
        """
        toggleSource(self, src_id, REQUEST = {}) => toggle enabled/disabled source
        """
        ids = self.objectIds('GRUFUsers')
        if src_id not in ids:
            raise ValueError, "Invalid source: '%s' (%s)" % (src_id, ids)
        src = getattr(self, src_id)
        if src.enabled:
            src.disableSource()
        else:
            src.enableSource()
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_GRUFSources')

    security.declareProtected(Permissions.manage_users, 'listUserSources')

    def listUserSources(self):
        """
        listUserSources(self, ) => Return a list of userfolder objects
        Only return VALID (ie containing an acl_users) user sources if all is None
        XXX HAS TO BE OPTIMIZED VERY MUCH!
        We add a check in debug mode to ensure that invalid sources won't be added
        to the list.
        This method return only _enabled_ user sources.
        """
        ret = []
        dret = {}
        if DEBUG_MODE:
            for src in self.objectValues(['GRUFUsers']):
                if not src.enabled:
                    continue
                if 'acl_users' in src.objectIds():
                    if getattr(aq_base(src.acl_users), 'authenticate', None):
                        dret[src.id] = src.acl_users

        for src in self.objectValues(['GRUFUsers']):
            if not src.enabled:
                continue
            if 'acl_users' not in src.objectIds():
                continue
            dret[src.id] = src.acl_users

        ret = dret.items()
        ret.sort()
        return [ src[1] for src in ret ]

    security.declareProtected(Permissions.manage_users, 'listUserSourceFolders')

    def listUserSourceFolders(self):
        """
        listUserSources(self, ) => Return a list of GRUFUsers objects
        """
        ret = []
        for src in self.objectValues(['GRUFUsers']):
            ret.append(src)

        ret.sort(lambda x, y: cmp(x.id, y.id))
        return ret

    security.declarePrivate('getUserSource')

    def getUserSource(self, id):
        """
        getUserSource(self, id) => GRUFUsers.acl_users object.
        Raises if no acl_users available
        """
        return getattr(self, id).acl_users

    security.declarePrivate('getUserSourceFolder')

    def getUserSourceFolder(self, id):
        """
        getUserSourceFolder(self, id) => GRUFUsers object
        """
        return getattr(self, id)

    security.declareProtected(Permissions.manage_users, 'addUserSource')

    def addUserSource(self, factory_uri, REQUEST={}, *args, **kw):
        """
        addUserSource(self, factory_uri, REQUEST = {}, *args, **kw) => redirect
        Adds the specified user folder
        """
        ids = self.objectIds('GRUFUsers')
        if ids:
            ids.sort()
            if ids == ['Users']:
                last = 0
            else:
                last = int(ids[(-1)][-2:])
            next_id = 'Users%02d' % (last + 1,)
        else:
            next_id = 'Users'
        uf = GRUFFolder.GRUFUsers(id=next_id)
        self._setObject(next_id, uf)
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect('%s/%s/%s' % (self.absolute_url(), next_id, factory_uri))
        return getattr(self, next_id).unrestrictedTraverse(factory_uri)(*args, **kw)

    addUserSource = postonly(addUserSource)
    security.declareProtected(Permissions.manage_users, 'deleteUserSource')

    def deleteUserSource(self, id=None, REQUEST={}):
        """
        deleteUserSource(self, id = None, REQUEST = {}) => Delete the specified user source
        """
        if type(id) != type('s'):
            raise ValueError, 'You must choose a valid source to delete and confirm it.'
        self.manage_delObjects([id])
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_GRUFSources')

    deleteUserSource = postonly(deleteUserSource)
    security.declareProtected(Permissions.manage_users, 'getDefaultUserSource')

    def getDefaultUserSource(self):
        """
        getDefaultUserSource(self,) => acl_users object
        Return default user source for user writing.
        XXX By now, the FIRST source is the default one. This may change in the future.
        """
        lst = self.listUserSources()
        if not lst:
            raise RuntimeError, 'No valid User Source to add users in.'
        return lst[0]

    security.declareProtected(Permissions.manage_users, 'listAvailableUserSources')

    def listAvailableUserSources(self, filter_permissions=1, filter_classes=1):
        """
        listAvailableUserSources(self, filter_permissions = 1, filter_classes = 1) => tuples (name, factory_uri)
        List UserFolder replacement candidates.

        - if filter_classes is true, return only ones which have a base UserFolder class
        - if filter_permissions, return only types the user has rights to add
        """
        ret = []
        user = getSecurityManager().getUser()
        meta_types = []
        if callable(self.all_meta_types):
            all = self.all_meta_types()
        else:
            all = self.all_meta_types
        for meta_type in all:
            if filter_permissions and meta_type.has_key('permission'):
                if user.has_permission(meta_type['permission'], self):
                    meta_types.append(meta_type)
            else:
                meta_types.append(meta_type)

        for t in meta_types:
            if t['name'] == self.meta_type:
                continue
            if filter_classes:
                try:
                    if t.get('instance', None) and t['instance'].isAUserFolder:
                        ret.append((t['name'], t['action']))
                        continue
                    if t.get('instance', None) and class_utility.isBaseClass(AccessControl.User.BasicUserFolder, t['instance']):
                        ret.append((t['name'], t['action']))
                        continue
                except AttributeError:
                    pass

            else:
                ret.append((t['name'], t['action']))

        return tuple(ret)

    security.declareProtected(Permissions.manage_users, 'moveUserSourceUp')

    def moveUserSourceUp(self, id, REQUEST={}):
        """
        moveUserSourceUp(self, id, REQUEST = {}) => used in management screens
        try to get ids as consistant as possible
        """
        ids = self.objectIds('GRUFUsers')
        ids.sort()
        if not ids or id not in ids:
            raise ValueError, "Invalid User Source: '%s'" % (id,)
        src_index = ids.index(id)
        if src_index == 0:
            raise ValueError, "Cannot move '%s'  User Source up." % (id,)
        dest_index = src_index - 1
        if ids[dest_index] == 'Users':
            dest_num = 0
        else:
            dest_num = int(ids[dest_index][-2:])
        src_num = dest_num + 1
        src_id = id
        if dest_num == 0:
            dest_id = 'Users'
        else:
            dest_id = 'Users%02d' % (dest_num,)
        tmp_id = '%s_' % (dest_id,)
        self._renameUserSource(src_id, tmp_id)
        self._renameUserSource(dest_id, src_id)
        self._renameUserSource(tmp_id, dest_id)
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_GRUFSources')

    moveUserSourceUp = postonly(moveUserSourceUp)
    security.declareProtected(Permissions.manage_users, 'moveUserSourceDown')

    def moveUserSourceDown(self, id, REQUEST={}):
        """
        moveUserSourceDown(self, id, REQUEST = {}) => used in management screens
        try to get ids as consistant as possible
        """
        ids = self.objectIds('GRUFUsers')
        ids.sort()
        if not ids or id not in ids:
            raise ValueError, "Invalid User Source: '%s'" % (id,)
        src_index = ids.index(id)
        if src_index == len(ids) - 1:
            raise ValueError, "Cannot move '%s'  User Source up." % (id,)
        dest_index = src_index + 1
        if id == 'Users':
            dest_num = 1
        else:
            dest_num = int(ids[dest_index][-2:])
        src_num = dest_num - 1
        src_id = id
        if dest_num == 0:
            dest_id = 'Users'
        else:
            dest_id = 'Users%02d' % (dest_num,)
        tmp_id = '%s_' % (dest_id,)
        self._renameUserSource(src_id, tmp_id)
        self._renameUserSource(dest_id, src_id)
        self._renameUserSource(tmp_id, dest_id)
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_GRUFSources')

    moveUserSourceDown = postonly(moveUserSourceDown)
    security.declarePrivate('_renameUserSource')

    def _renameUserSource(self, id, new_id):
        """
        Rename a particular sub-object.
        Taken fro CopySupport.manage_renameObject() code, modified to disable verifications.
        """
        try:
            self._checkId(new_id)
        except:
            raise CopyError, MessageDialog(title='Invalid Id', message=sys.exc_info()[1], action='manage_main')

        ob = self._getOb(id)
        try:
            ob._notifyOfCopyTo(self, op=1)
        except:
            raise CopyError, MessageDialog(title='Rename Error', message=sys.exc_info()[1], action='manage_main')

        self._delObject(id)
        ob = aq_base(ob)
        ob._setId(new_id)
        self._setObject(new_id, ob, set_owner=0)

    security.declareProtected(Permissions.manage_users, 'replaceUserSource')

    def replaceUserSource(self, id=None, new_factory=None, REQUEST={}, *args, **kw):
        """
        replaceUserSource(self, id = None, new_factory = None, REQUEST = {}, *args, **kw) => perform user source replacement

        If new_factory is None, find it inside REQUEST (useful for ZMI screens)
        """
        if type(id) != type('s'):
            raise ValueError, 'You must choose a valid source to replace and confirm it.'
        if not new_factory:
            for record in REQUEST.get('source_rec', []):
                if record['id'] == id:
                    new_factory = record['new_factory']
                    break

            if not new_factory:
                raise ValueError, 'You must select a new User Folder type.'
        us = getattr(self, id)
        if 'acl_users' in us.objectIds():
            us.manage_delObjects(['acl_users'])
        if REQUEST.has_key('RESPONSE'):
            return REQUEST.RESPONSE.redirect('%s/%s/%s' % (self.absolute_url(), id, new_factory))
        return us.unrestrictedTraverse(new_factory)(*args, **kw)

    replaceUserSource = postonly(replaceUserSource)
    security.declareProtected(Permissions.manage_users, 'hasLDAPUserFolderSource')

    def hasLDAPUserFolderSource(self):
        """
        hasLDAPUserFolderSource(self,) => boolean
        Return true if a LUF source is instanciated.
        """
        for src in self.listUserSources():
            if src.meta_type == 'LDAPUserFolder':
                return 1

        return

    security.declareProtected(Permissions.manage_users, 'updateLDAPUserFolderMapping')

    def updateLDAPUserFolderMapping(self, REQUEST=None):
        """
        updateLDAPUserFolderMapping(self, REQUEST = None) => None

        Update the first LUF source in the process so that LDAP-group-to-Zope-role mapping
        is done.
        This is done by calling the appropriate method in LUF and affecting all 'group_' roles
        to the matching LDAP groups.
        """
        groups = self.getGroupIds()
        for src in self.listUserSources():
            if not src.meta_type == 'LDAPUserFolder':
                continue
            deletes = []
            for (grp, role) in src.getGroupMappings():
                if role.startswith('group_'):
                    deletes.append(grp)

            src.manage_deleteGroupMappings(deletes)
            ldap_groups = src.getGroups(attr='cn')
            for grp in groups:
                if src._local_groups:
                    grp_name = grp
                else:
                    grp_name = grp[len('group_'):]
                Log(LOG_DEBUG, 'cheching', grp_name, 'in', ldap_groups)
                if grp_name not in ldap_groups:
                    continue
                Log(LOG_DEBUG, 'Map', grp, 'to', grp_name)
                src.manage_addGroupMapping(grp_name, grp)

        if REQUEST:
            return REQUEST.RESPONSE.redirect(self.absolute_url() + '/manage_wizard')
        updateLDAPUserFolderMapping = postonly(updateLDAPUserFolderMapping)

    def listLDAPUserFolderMapping(self):
        """
        listLDAPUserFolderMapping(self,) => utility method
        """
        ret = []
        gruf_done = []
        ldap_done = []
        for src in self.listUserSources():
            if not src.meta_type == 'LDAPUserFolder':
                continue
            if src._local_groups:
                gruf_ids = self.getGroupIds()
            else:
                gruf_ids = self.getGroupIds()
            ldap_mapping = src.getGroupMappings()
            ldap_groups = src.getGroups(attr='cn')
            for (grp, role) in ldap_mapping:
                if role in gruf_ids:
                    ret.append((role, grp))
                    gruf_done.append(role)
                    ldap_done.append(grp)
                    if not src._local_groups:
                        ldap_done.append(role)

            for grp in ldap_groups:
                if grp not in ldap_done:
                    ret.append((None, grp))

            for grp in gruf_ids:
                if grp not in gruf_done:
                    ret.append((grp, None))

            Log(LOG_DEBUG, 'return', ret)
            return ret

        return

    security.declareProtected(Permissions.manage_users, 'getInvalidMappings')

    def getInvalidMappings(self):
        """
        return true if LUF mapping looks good
        """
        wrong = []
        grufs = []
        for (gruf, ldap) in self.listLDAPUserFolderMapping():
            if gruf and ldap:
                continue
            if not gruf:
                continue
            if gruf.startswith('group_'):
                gruf = gruf[len('group_'):]
            grufs.append(gruf)

        for (gruf, ldap) in self.listLDAPUserFolderMapping():
            if gruf and ldap:
                continue
            if not ldap:
                continue
            if ldap.startswith('group_'):
                ldap = ldap[len('group_'):]
            if ldap in grufs:
                wrong.append(ldap)

        return wrong

    security.declareProtected(Permissions.manage_users, 'getLUFSource')

    def getLUFSource(self):
        """
        getLUFSource(self,) => Helper to get a pointer to the LUF src.
        Return None if not available
        """
        for src in self.listUserSources():
            if src.meta_type == 'LDAPUserFolder':
                return src

    security.declareProtected(Permissions.manage_users, 'areLUFGroupsLocal')

    def areLUFGroupsLocal(self):
        """return true if luf groups are stored locally"""
        return hasattr(self.getLUFSource(), '_local_groups')

    security.declareProtected(Permissions.manage_users, 'haveLDAPGroupFolder')

    def haveLDAPGroupFolder(self):
        """return true if LDAPGroupFolder is the groups source
        """
        return not not self.Groups.acl_users.meta_type == 'LDAPGroupFolder'


class treeWrapper:
    """
    treeWrapper: Wrapper around user/group objects for the tree
    """
    __module__ = __name__

    def __init__(self, id, tree, parents=[]):
        """
        __init__(self, id, tree, parents = []) => wraps the user object for dtml-tree
        """
        self._id = id
        self.name = tree[id]['name']
        self.icon = tree[id]['icon']
        self.is_group = tree[id]['is_group']
        parents.append(id)
        self.path = parents
        subobjects = []
        for grp_id in tree.keys():
            if id in tree[grp_id]['belongs_to']:
                subobjects.append(treeWrapper(grp_id, tree, parents))

        subobjects.sort(lambda x, y: cmp(x.sortId(), y.sortId()))
        self.subobjects = subobjects

    def id(self):
        return self.name

    def sortId(self):
        if self.is_group:
            return '__%s' % (self._id,)
        else:
            return self._id

    def tpValues(self):
        """
        Return 'subobjects'
        """
        return self.subobjects

    def tpId(self):
        return self._id

    def tpURL(self):
        return self.tpId()


InitializeClass(GroupUserFolder)