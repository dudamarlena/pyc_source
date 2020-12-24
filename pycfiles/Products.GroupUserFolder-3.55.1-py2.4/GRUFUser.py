# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/GRUFUser.py
# Compiled at: 2008-05-20 04:51:58
"""

"""
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from copy import copy
from Globals import MessageDialog, DTMLFile
from AccessControl import ClassSecurityInfo
from AccessControl import Permissions
from AccessControl import getSecurityManager
from Globals import InitializeClass
from Acquisition import Implicit, aq_inner, aq_parent, aq_base
from Globals import Persistent
from AccessControl.Role import RoleManager
from OFS.SimpleItem import Item
from OFS.PropertyManager import PropertyManager
from OFS import ObjectManager, SimpleItem
from DateTime import DateTime
from App import ImageFile
import AccessControl.Role, webdav.Collection, Products, os, string, shutil, random
from global_symbols import *
import AccessControl
from Products.GroupUserFolder import postonly
import GRUFFolder, GroupUserFolder
from AccessControl.PermissionRole import _what_not_even_god_should_do, rolesForPermissionOn
from ComputedAttribute import ComputedAttribute
import os, traceback
from interfaces.IUserFolder import IUser, IGroup
_marker = [
 'INVALID_VALUE']

class GRUFUserAtom(AccessControl.User.BasicUser, Implicit):
    """
    Base class for all GRUF-catched User objects.
    There's, alas, many copy/paste from AccessControl.BasicUser...
    """
    __module__ = __name__
    security = ClassSecurityInfo()
    security.declarePrivate('_setUnderlying')

    def _setUnderlying(self, user):
        """
        _setUnderlying(self, user) => Set the GRUFUser properties to
        the underlying user's one.
        Be careful that any change to the underlying user won't be
        reported here. $$$ We don't know yet if User object are
        transaction-persistant or not...
        """
        self._original_name = user.getUserName()
        self._original_password = user._getPassword()
        self._original_roles = user.getRoles()
        self._original_domains = user.getDomains()
        self._original_id = user.getId()
        self.__underlying__ = user

    security.declarePrivate('__init__')

    def __init__(self, underlying_user, GRUF, isGroup, source_id):
        self._setUnderlying(underlying_user)
        self._isGroup = isGroup
        self._GRUF = GRUF
        self._source_id = source_id
        self.id = self._original_id
        self.clearCachedGroupsAndRoles()

    security.declarePrivate('clearCachedGroupsAndRoles')

    def clearCachedGroupsAndRoles(self, underlying_user=None):
        self._groups = None
        self._user_roles = None
        self._group_roles = None
        self._all_roles = None
        if underlying_user:
            self._setUnderlying(underlying_user)
        self._original_user_roles = None
        return

    security.declarePublic('isGroup')

    def isGroup(self):
        """Return 1 if this user is a group abstraction"""
        return self._isGroup

    security.declarePublic('getUserSourceId')

    def getUserSourceId(self):
        """
        getUserSourceId(self,) => string
        Return the GRUF's GRUFUsers folder used to fetch this user.
        """
        return self._source_id

    security.declarePrivate('getGroupNames')

    def getGroupNames(self):
        """..."""
        ret = self._getGroups(no_recurse=1)
        return map(lambda x: x[GROUP_PREFIX_LEN:], ret)

    security.declarePrivate('getGroupIds')

    def getGroupIds(self):
        """..."""
        return list(self._getGroups(no_recurse=1))

    security.declarePrivate('getAllGroups')

    def getAllGroups(self):
        """Same as getAllGroupNames()"""
        return self.getAllGroupIds()

    security.declarePrivate('getAllGroupNames')

    def getAllGroupNames(self):
        """..."""
        ret = self._getGroups()
        return map(lambda x: x[GROUP_PREFIX_LEN:], ret)

    security.declarePrivate('getAllGroupIds')

    def getAllGroupIds(self):
        """..."""
        return list(self._getGroups())

    security.declarePrivate('getGroups')

    def getGroups(self, *args, **kw):
        """..."""
        ret = self._getGroups(*args, **kw)
        return list(ret)

    security.declarePrivate('getImmediateGroups')

    def getImmediateGroups(self):
        """
        Return NON-TRANSITIVE groups
        """
        ret = self._getGroups(no_recurse=1)
        return list(ret)

    def _getGroups(self, no_recurse=0, already_done=None, prefix=GROUP_PREFIX):
        """
        getGroups(self, no_recurse = 0, already_done = None, prefix = GROUP_PREFIX) => list of strings
        
        If this user is a user (uh, uh), get its groups.
        THIS METHODS NOW SUPPORTS NESTED GROUPS ! :-)
        The already_done parameter prevents infite recursions.
        Keep it as it is, never give it a value.

        If no_recurse is true, return only first level groups

        This method is private and should remain so.
        """
        if already_done is None:
            already_done = []
        if self._groups is not None:
            return self._groups
        if self._original_user_roles is None:
            self._original_user_roles = self.__underlying__.getRoles()
        ret = []
        for role in self._original_user_roles:
            if role.startswith(prefix):
                if self._isGroup and role in already_done:
                    continue
                grp = self.aq_parent.getUser(role)
                if not grp:
                    continue
                if role in ret:
                    continue
                ret.append(role)
                if no_recurse:
                    continue
                for extend in grp.getGroups(already_done=ret):
                    if extend not in ret:
                        ret.append(extend)

        self._groups = tuple(ret)
        return self._groups

    security.declarePrivate('getGroupsWithoutPrefix')

    def getGroupsWithoutPrefix(self, **kw):
        """
        Same as getGroups but return them without a prefix.
        """
        ret = []
        for group in self.getGroups(**kw):
            if group.startswith(GROUP_PREFIX):
                ret.append(group[len(GROUP_PREFIX):])

        return ret

    security.declarePublic('getUserNameWithoutGroupPrefix')

    def getUserNameWithoutGroupPrefix(self):
        """Return the username of a user without a group prefix"""
        if self.isGroup() and self._original_name[:len(GROUP_PREFIX)] == GROUP_PREFIX:
            return self._original_name[len(GROUP_PREFIX):]
        return self._original_name

    security.declarePublic('getUserId')

    def getUserId(self):
        """Return the user id of a user"""
        if self.isGroup() and not self._original_name[:len(GROUP_PREFIX)] == GROUP_PREFIX:
            return '%s%s' % (GROUP_PREFIX, self._original_name)
        return self._original_name

    security.declarePublic('getName')

    def getName(self):
        """Get user's or group's name.
        For a user, the name can be set by the underlying user folder but usually id == name.
        For a group, the ID is prefixed, but the NAME is NOT prefixed by 'group_'.
        """
        return self.getUserNameWithoutGroupPrefix()

    security.declarePublic('getUserName')

    def getUserName(self):
        """Alias for getName()"""
        return self.getUserNameWithoutGroupPrefix()

    security.declarePublic('getId')

    def getId(self, unprefixed=0):
        """Get the ID of the user. The ID can be used, at least from
        Python, to get the user from the user's UserDatabase
        """
        if self.isGroup() and not self._original_name.startswith(GROUP_PREFIX) and not unprefixed:
            return '%s%s' % (GROUP_PREFIX, self._original_name)
        return self._original_name

    security.declarePublic('getRoles')

    def getRoles(self):
        """
        Return the list (tuple) of roles assigned to a user.
        THIS IS WHERE THE ATHENIANS REACHED !
        """
        if self._all_roles is not None:
            return self._all_roles
        self._all_roles = GroupUserFolder.unique(self.getUserRoles() + self.getGroupRoles())
        return self._all_roles

    security.declarePublic('getUserRoles')

    def getUserRoles(self):
        """
        returns the roles defined for the user without the group roles
        """
        if self._user_roles is not None:
            return self._user_roles
        prefix = GROUP_PREFIX
        if self._original_user_roles is None:
            self._original_user_roles = self.__underlying__.getRoles()
        self._user_roles = tuple([ r for r in self._original_user_roles if not r.startswith(prefix) ])
        return self._user_roles

    security.declarePublic('getGroupRoles')

    def getGroupRoles(self):
        """
        Return the tuple of roles belonging to this user's group(s)
        """
        if self._group_roles is not None:
            return self._group_roles
        ret = []
        acl_users = self._GRUF.acl_users
        groups = acl_users.getGroupIds()
        for group in self.getGroups():
            if group not in groups:
                Log('Group', group, 'is invalid. Ignoring.')
                continue
            ret.extend(acl_users.getGroup(group).getUserRoles())

        self._group_roles = GroupUserFolder.unique(ret)
        return self._group_roles

    security.declarePublic('getRolesInContext')

    def getRolesInContext(self, object, userid=None):
        """
        Return the list of roles assigned to the user,
        including local roles assigned in context of
        the passed in object.
        """
        if not userid:
            userid = self.getId()
        roles = {}
        for role in self.getRoles():
            roles[role] = 1

        user_groups = self.getGroups()
        inner_obj = getattr(object, 'aq_inner', object)
        while 1:
            local_roles = getattr(inner_obj, '__ac_local_roles__', None)
            if local_roles:
                if callable(local_roles):
                    local_roles = local_roles()
                dict = local_roles or {}
                for role in dict.get(userid, []):
                    roles[role] = 1

                for groupid in user_groups:
                    for role in dict.get(groupid, []):
                        roles[role] = 1

            obj = getattr(inner_obj, 'aq_base', inner_obj)
            if getattr(obj, '__ac_local_roles_block__', None):
                break
            inner = getattr(inner_obj, 'aq_inner', inner_obj)
            parent = getattr(inner, 'aq_parent', None)
            if parent is not None:
                inner_obj = parent
                continue
            if hasattr(inner_obj, 'im_self'):
                inner_obj = inner_obj.im_self
                inner_obj = getattr(inner_obj, 'aq_inner', inner_obj)
                continue
            break

        return tuple(roles.keys())

    security.declarePublic('getDomains')

    def getDomains(self):
        """Return the list of domain restrictions for a user"""
        return self._original_domains

    security.declarePrivate('getProperty')

    def getProperty(self, name, default=_marker):
        """getProperty(self, name) => return property value or raise AttributeError
        """
        v = getattr(self.__underlying__, name, default)
        if v is _marker:
            raise AttributeError, name
        return v

    security.declarePrivate('hasProperty')

    def hasProperty(self, name):
        """hasProperty"""
        return hasattr(self.__underlying__, name)

    security.declarePrivate('setProperty')

    def setProperty(self, name, value):
        """setProperty => Try to set the property...
        By now, it's available only for LDAPUserFolder
        """
        src = self._GRUF.getUserSource(self.getUserSourceId())
        if not src:
            raise RuntimeError, "Invalid or missing user source for '%s'." % (self.getId(),)
        if hasattr(src, 'manage_setUserProperty'):
            ldapname = None
            for schema in src.getSchemaConfig().values():
                if schema['ldap_name'] == name:
                    ldapname = schema['ldap_name']
                if schema['public_name'] == name:
                    ldapname = schema['ldap_name']
                    break

            if ldapname is None:
                raise KeyError, "Invalid LDAP attribute: '%s'." % (name,)
            user_dn = src._find_user_dn(self.getUserName())
            src.manage_setUserProperty(user_dn, ldapname, value)
            self.__underlying__ = src.getUser(self.getId())
            if not self.__underlying__:
                raise RuntimeError, "Error while setting property of '%s'." % (self.getId(),)
        if not self.hasProperty(name):
            raise NotImplementedError, "Property setting is not supported for '%s'." % (name,)
        v = self._GRUF.getUserById(self.getId()).getProperty(name)
        if not v == value:
            Log(LOG_DEBUG, "Property '%s' for user '%s' should be '%s' and not '%s'" % (name, self.getId(), value, v))
            raise NotImplementedError, "Property setting is not supported for '%s'." % (name,)
        return

    security.declarePrivate('authenticate')

    def authenticate(self, password, request):
        if self._isGroup:
            return
        return self.__underlying__.authenticate(password, request)

    security.declarePublic('allowed')

    def allowed(self, object, object_roles=None):
        """Check whether the user has access to object. The user must
           have one of the roles in object_roles to allow access."""
        if object_roles is _what_not_even_god_should_do:
            return 0
        if object_roles is None or 'Anonymous' in object_roles:
            return 1
        if 'Authenticated' in object_roles and self.getUserName() != 'Anonymous User':
            return 1
        if 'Shared' in object_roles:
            object_roles = self._shared_roles(object)
            if object_roles is None or 'Anonymous' in object_roles:
                return 1
        object_roles_dict = {}
        for role in object_roles:
            object_roles_dict[role] = 1

        if [ role for role in self.getUserRoles() if object_roles_dict.has_key(role) ]:
            if self._check_context(object):
                return 1
            return
        if [ role for role in self.getGroupRoles() if object_roles_dict.has_key(role) ]:
            if self._check_context(object):
                return 1
            return
        user_groups = self.getGroups()
        inner_obj = getattr(object, 'aq_inner', object)
        userid = self.getId()
        while 1:
            local_roles = getattr(inner_obj, '__ac_local_roles__', None)
            if local_roles:
                if callable(local_roles):
                    local_roles = local_roles()
                dict = local_roles or {}
                if [ role for role in dict.get(userid, []) if object_roles_dict.has_key(role) ]:
                    if self._check_context(object):
                        return 1
                    return
                for groupid in user_groups:
                    if [ role for role in dict.get(groupid, []) if object_roles_dict.has_key(role) ]:
                        if self._check_context(object):
                            return 1
                        return

            obj = getattr(inner_obj, 'aq_base', inner_obj)
            if getattr(obj, '__ac_local_roles_block__', None):
                break
            inner = getattr(inner_obj, 'aq_inner', inner_obj)
            parent = getattr(inner, 'aq_parent', None)
            if parent is not None:
                inner_obj = parent
                continue
            if hasattr(inner_obj, 'im_self'):
                inner_obj = inner_obj.im_self
                inner_obj = getattr(inner_obj, 'aq_inner', inner_obj)
                continue
            break

        return

    security.declarePublic('hasRole')

    def hasRole(self, *args, **kw):
        """hasRole is an alias for 'allowed' and has been deprecated.

        Code still using this method should convert to either 'has_role' or
        'allowed', depending on the intended behaviour.

        """
        import warnings
        warnings.warn('BasicUser.hasRole is deprecated, please use BasicUser.allowed instead; hasRole was an alias for allowed, but you may have ment to use has_role.', DeprecationWarning)
        return self.allowed(*args, **kw)

    def __getattr__(self, name):
        ret = getattr(self.__dict__['__underlying__'], name)
        return ret

    security.declarePublic('getUnwrappedUser')

    def getUnwrappedUser(self):
        """
        same as GRUF.getUnwrappedUser, but implicitly with this particular user
        """
        return self.__dict__['__underlying__']

    def __getitem__(self, name):
        return self.__underlying__[name]

    def asHTML(self, implicit=0):
        """
        asHTML(self, implicit=0) => HTML string
        Used to generate homogeneous links for management screens
        """
        acl_users = self.acl_users
        if self.isGroup():
            color = acl_users.group_color
            kind = 'Group'
        else:
            color = acl_users.user_color
            kind = 'User'
        ret = '<a href="%(href)s" alt="%(alt)s"><font color="%(color)s">%(name)s</font></a>' % {'color': color, 'href': '%s/%s/manage_workspace?FORCE_USER=1' % (acl_users.absolute_url(), self.getId()), 'name': self.getUserNameWithoutGroupPrefix(), 'alt': '%s (%s)' % (self.getUserNameWithoutGroupPrefix(), kind)}
        if implicit:
            return '<i>%s</i>' % ret
        return ret

    security.declarePrivate('isInGroup')

    def isInGroup(self, groupid):
        """Return true if the user is member of the specified group id
        (including transitive groups)"""
        return groupid in self.getAllGroupIds()

    security.declarePublic('getRealId')

    def getRealId(self):
        """Return id WITHOUT group prefix
        """
        raise NotImplementedError, 'Must be derived in subclasses'


class GRUFUser(GRUFUserAtom):
    """
    This is the class for actual user objects
    """
    __module__ = __name__
    __implements__ = (
     IUser,)
    security = ClassSecurityInfo()
    security.declarePublic('changePassword')

    def changePassword(self, password, REQUEST=None):
        """Set the user's password. This method performs its own security checks"""
        user = getSecurityManager().getUser()
        if not user.has_permission(Permissions.manage_users, self._GRUF):
            if user.__class__.__name__ != 'GRUFUser':
                raise 'Unauthorized', "You cannot change someone else's password."
            if not user.getId() == self.getId():
                raise 'Unauthorized', "You cannot change someone else's password."
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userSetPassword(self.getId(), password)

    changePassword = postonly(changePassword)
    security.declarePrivate('setRoles')

    def setRoles(self, roles):
        """Change the roles of a user atom.
        """
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userSetRoles(self.getId(), roles)

    security.declarePrivate('addRole')

    def addRole(self, role):
        """Append a role for a user atom
        """
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userAddRole(self.getId(), role)

    security.declarePrivate('removeRole')

    def removeRole(self, role):
        """Remove the role of a user atom
        """
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userRemoveRole(self.getId(), role)

    security.declarePrivate('setPassword')

    def setPassword(self, newPassword):
        """Set the password of a user
        """
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userSetPassword(self.getId(), newPassword)

    security.declarePrivate('setDomains')

    def setDomains(self, domains):
        """Set domains for a user
        """
        self.clearCachedGroupsAndRoles()
        self._GRUF.userSetDomains(self.getId(), domains)
        self._original_domains = self._GRUF.userGetDomains(self.getId())

    security.declarePrivate('addDomain')

    def addDomain(self, domain):
        """Append a domain to a user
        """
        self.clearCachedGroupsAndRoles()
        self._GRUF.userAddDomain(self.getId(), domain)
        self._original_domains = self._GRUF.userGetDomains(self.getId())

    security.declarePrivate('removeDomain')

    def removeDomain(self, domain):
        """Remove a domain from a user
        """
        self.clearCachedGroupsAndRoles()
        self._GRUF.userRemoveDomain(self.getId(), domain)
        self._original_domains = self._GRUF.userGetDomains(self.getId())

    security.declarePrivate('setGroups')

    def setGroups(self, groupnames):
        """Set the groups of a user
        """
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userSetGroups(self.getId(), groupnames)

    security.declarePrivate('addGroup')

    def addGroup(self, groupname):
        """add a group to a user atom
        """
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userAddGroup(self.getId(), groupname)

    security.declarePrivate('removeGroup')

    def removeGroup(self, groupname):
        """remove a group from a user atom.
        """
        self.clearCachedGroupsAndRoles()
        return self._GRUF.userRemoveGroup(self.getId(), groupname)

    security.declarePrivate('_getPassword')

    def _getPassword(self):
        """Return the password of the user."""
        return self._original_password

    security.declarePublic('getRealId')

    def getRealId(self):
        """Return id WITHOUT group prefix
        """
        return self.getId()


class GRUFGroup(GRUFUserAtom):
    """
    This is the class for actual group objects
    """
    __module__ = __name__
    __implements__ = (
     IGroup,)
    security = ClassSecurityInfo()
    security.declarePublic('getRealId')

    def getRealId(self):
        """Return group id WITHOUT group prefix
        """
        return self.getId()[len(GROUP_PREFIX):]

    def _getLDAPMemberIds(self):
        """
        _getLDAPMemberIds(self,) => Uses LDAPUserFolder to find
        users in a group.
        """
        gruf = self.aq_parent
        src = None
        for src in gruf.listUserSources():
            if not src.meta_type == 'LDAPUserFolder':
                continue

        if src is None:
            Log(LOG_DEBUG, 'No LDAPUserFolder source found')
            return []
        groups = src.getGroups()
        groupid = self.getId()
        grp = [ group for group in groups if group[0] == self.getId() ]
        if not grp:
            Log(LOG_DEBUG, "No such group ('%s') found." % (groupid,))
            return []
        userids = src.getGroupedUsers(grp)
        Log(LOG_DEBUG, "We've found %d users belonging to the group '%s'" % (len(userids), grp))
        return userids

    def _getMemberIds(self, users=1, groups=1, transitive=1):
        """
        Return the member ids (users and groups) of the atoms of this group.
        Transitiveness attribute is ignored with LDAP (no nested groups with
        LDAP anyway).
        This method now uses a shortcut to fetch members of an LDAP group
        (stored either within Zope or within your LDAP server)
        """
        gruf = self.aq_parent
        ldap_sources = []
        lst = []
        if transitive:
            method = 'getAllGroupIds'
        else:
            method = 'getGroupIds'
        if users:
            for src in gruf.listUserSources():
                if src.meta_type == 'LDAPUserFolder':
                    ldap_sources.append(src)
                    continue
                lst.extend(src.getUserNames())

        if groups:
            lst.extend(gruf.getGroupIds())
        groupid = self.getId()
        groups_mapping = {}
        for u in lst:
            usr = gruf.getUser(u)
            if not usr:
                groups_mapping[u] = []
                Log(LOG_WARNING, 'Invalid user retreiving:', u)
            else:
                groups_mapping[u] = getattr(usr, method)()

        members = [ u for u in lst if groupid in groups_mapping[u] ]
        groupid = self.getId()
        for src in ldap_sources:
            groups = src.getGroups()
            grp = [ group for group in groups if group[0] == self.getId() or GROUP_PREFIX + group[0] == self.getId() ]
            if not grp:
                Log(LOG_DEBUG, "No such group ('%s') found." % (groupid,))
                continue
            userids = [ str(u) for u in src.getGroupedUsers(grp) ]
            Log(LOG_DEBUG, "We've found %d users belonging to the group '%s'" % (len(userids), grp))
            members.extend(userids)

        return members

    security.declarePrivate('getMemberIds')

    def getMemberIds(self, transitive=1):
        """Return member ids of this group, including or not transitive groups."""
        return self._getMemberIds(transitive=transitive)

    security.declarePrivate('getUserMemberIds')

    def getUserMemberIds(self, transitive=1):
        """Return the member ids (users only) of the users of this group"""
        return self._getMemberIds(groups=0, transitive=transitive)

    security.declarePrivate('getGroupMemberIds')

    def getGroupMemberIds(self, transitive=1):
        """Return the members ids (groups only) of the groups of this group"""
        return self._getMemberIds(users=0, transitive=transitive)

    security.declarePrivate('hasMember')

    def hasMember(self, id):
        """Return true if the specified atom id is in the group.
        This is the contrary of IUserAtom.isInGroup(groupid)"""
        gruf = self.aq_parent
        return id in gruf.getMemberIds(self.getId())

    security.declarePrivate('addMember')

    def addMember(self, userid):
        """Add a user the the current group"""
        gruf = self.aq_parent
        groupid = self.getId()
        usr = gruf.getUser(userid)
        if not usr:
            raise ValueError, "Invalid user: '%s'" % (userid,)
        if groupid not in gruf.getGroupNames() + gruf.getGroupIds():
            raise ValueError, "Invalid group: '%s'" % (groupid,)
        groups = list(usr.getGroups())
        groups.append(groupid)
        groups = GroupUserFolder.unique(groups)
        return gruf._updateUser(userid, groups=groups)

    security.declarePrivate('removeMember')

    def removeMember(self, userid):
        """Remove a user from the current group"""
        gruf = self.aq_parent
        groupid = self.getId()
        usr = gruf.getUser(userid)
        if not usr:
            raise ValueError, "Invalid user: '%s'" % (userid,)
        groups = list(usr.getImmediateGroups())
        if groupid in groups:
            groups.remove(groupid)
            gruf._updateUser(userid, groups=groups)
        else:
            raise ValueError, "User '%s' doesn't belong to group '%s'" % (userid, groupid)

    security.declarePrivate('setMembers')

    def setMembers(self, userids):
        """Set the members of the group
        """
        member_ids = self.getMemberIds()
        all_ids = copy(member_ids)
        all_ids.extend(userids)
        groupid = self.getId()
        for id in all_ids:
            if id in member_ids and id not in userids:
                self.removeMember(id)
            elif id not in member_ids and id in userids:
                self.addMember(id)


InitializeClass(GRUFUser)
InitializeClass(GRUFGroup)