# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/GroupDataTool.py
# Compiled at: 2008-05-20 04:51:58
"""
Basic group data tool.
"""
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from Products.CMFCore.utils import UniqueObject, getToolByName
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Globals import DTMLFile
from Globals import InitializeClass
from AccessControl.Role import RoleManager
from BTrees.OOBTree import OOBTree
from ZPublisher.Converters import type_converters
from Acquisition import aq_inner, aq_parent, aq_base
from AccessControl import ClassSecurityInfo, Permissions, Unauthorized, getSecurityManager
from Products.CMFCore.ActionProviderBase import ActionProviderBase
try:
    from Products.CMFCore.permissions import ManagePortal
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ManagePortal

from Products.CMFCore.MemberDataTool import CleanupTemp
from interfaces.portal_groupdata import portal_groupdata as IGroupDataTool
from interfaces.portal_groupdata import GroupData as IGroupData
from Products.GroupUserFolder import postonly
from Products.GroupUserFolder.GRUFUser import GRUFGroup
_marker = []
from global_symbols import *

class GroupDataTool(UniqueObject, SimpleItem, PropertyManager, ActionProviderBase):
    """ This tool wraps group objects, allowing transparent access to properties.
    """
    __module__ = __name__
    __implements__ = (
     IGroupDataTool, getattr(ActionProviderBase, '__implements__', ()))
    id = 'portal_groupdata'
    meta_type = 'CMF Group Data Tool'
    _actions = ()
    _v_temps = None
    _properties = ({'id': 'title', 'type': 'string', 'mode': 'wd'},)
    security = ClassSecurityInfo()
    manage_options = ActionProviderBase.manage_options + ({'label': 'Overview', 'action': 'manage_overview'},) + PropertyManager.manage_options + SimpleItem.manage_options
    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = DTMLFile('dtml/explainGroupDataTool', globals())

    def __init__(self):
        self._members = OOBTree()
        self._setProperty('description', '', 'text')
        self._setProperty('email', '', 'string')

    security.declarePrivate('wrapGroup')

    def wrapGroup(self, g):
        """Returns an object implementing the GroupData interface"""
        id = g.getId()
        members = self._members
        if not members.has_key(id):
            temps = self._v_temps
            if temps is not None and temps.has_key(id):
                portal_group = temps[id]
            else:
                base = aq_base(self)
                portal_group = GroupData(base, id)
                if temps is None:
                    self._v_temps = {id: portal_group}
                    if hasattr(self, 'REQUEST'):
                        self.REQUEST._hold(CleanupTemp(self))
                else:
                    temps[id] = portal_group
        else:
            portal_group = members[id]
        return portal_group.__of__(self).__of__(g)

    security.declarePrivate('registerGroupData')

    def registerGroupData(self, g, id):
        """
        Adds the given member data to the _members dict.
        This is done as late as possible to avoid side effect
        transactions and to reduce the necessary number of
        entries.
        """
        self._members[id] = aq_base(g)


InitializeClass(GroupDataTool)

class GroupData(SimpleItem):
    __module__ = __name__
    __implements__ = IGroupData
    security = ClassSecurityInfo()
    id = None
    _tool = None

    def __init__(self, tool, id):
        self.id = id
        self._tool = tool

    def _getGRUF(self):
        return self.acl_users

    security.declarePrivate('notifyModified')

    def notifyModified(self):
        tool = getattr(self, '_tool', None)
        if tool is not None:
            del self._tool
            tool.registerGroupData(self, self.getId())
        return

    security.declarePublic('getGroup')

    def getGroup(self):
        """ Returns the actual group implementation. Varies by group
        implementation (GRUF/Nux/et al). In GRUF this is a user object."""
        parent = aq_parent(self)
        bcontext = aq_base(parent)
        bcontainer = aq_base(aq_parent(aq_inner(self)))
        if bcontext is bcontainer or not hasattr(bcontext, 'getUserName'):
            raise 'GroupDataError', "Can't find group data"
        return parent

    def getTool(self):
        return aq_parent(aq_inner(self))

    security.declarePublic('getGroupMemberIds')

    def getGroupMemberIds(self):
        """
        Return a list of group member ids
        """
        return map(lambda x: x.getMemberId(), self.getGroupMembers())

    security.declarePublic('getAllGroupMemberIds')

    def getAllGroupMemberIds(self):
        """
        Return a list of group member ids
        """
        return map(lambda x: x.getMemberId(), self.getAllGroupMembers())

    security.declarePublic('getGroupMembers')

    def getGroupMembers(self):
        """
        Returns a list of the portal_memberdata-ish members of the group.
        This doesn't include TRANSITIVE groups/users.
        """
        md = self.portal_memberdata
        gd = self.portal_groupdata
        ret = []
        for u_name in self.getGroup().getMemberIds(transitive=0):
            usr = self._getGRUF().getUserById(u_name)
            if not usr:
                raise AssertionError, 'Cannot retreive a user by its id !'
            if usr.isGroup():
                ret.append(gd.wrapGroup(usr))
            else:
                ret.append(md.wrapUser(usr))

        return ret

    security.declarePublic('getAllGroupMembers')

    def getAllGroupMembers(self):
        """
        Returns a list of the portal_memberdata-ish members of the group.
        This will include transitive groups / users
        """
        md = self.portal_memberdata
        gd = self.portal_groupdata
        ret = []
        for u_name in self.getGroup().getMemberIds():
            usr = self._getGRUF().getUserById(u_name)
            if not usr:
                raise AssertionError, 'Cannot retreive a user by its id !'
            if usr.isGroup():
                ret.append(gd.wrapGroup(usr))
            else:
                ret.append(md.wrapUser(usr))

        return ret

    def _getGroup(self):
        """
        _getGroup(self,) => Get the underlying group object
        """
        return self._getGRUF().getGroupByName(self.getGroupName())

    security.declarePrivate('canAdministrateGroup')

    def canAdministrateGroup(self):
        """
        Return true if the #current# user can administrate this group
        """
        user = getSecurityManager().getUser()
        tool = self.getTool()
        portal = getToolByName(tool, 'portal_url').getPortalObject()
        if user.has_permission(Permissions.manage_users, portal):
            return True
        managers = self.getProperty('delegated_group_member_managers', ())
        if user.getId() in managers:
            return True
        meth = getattr(user, 'getAllGroupNames', None)
        if meth:
            groups = meth()
        else:
            groups = ()
        for v in groups:
            if v in managers:
                return True

        return False

    security.declarePublic('addMember')

    def addMember(self, id, REQUEST=None):
        """ Add the existing member with the given id to the group"""
        if not self.canAdministrateGroup():
            raise Unauthorized, 'You cannot add a member to the group.'
        self._getGroup().addMember(id)
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getMemberById(id)
        if member:
            member.notifyModified()

    addMember = postonly(addMember)
    security.declarePublic('removeMember')

    def removeMember(self, id, REQUEST=None):
        """Remove the member with the provided id from the group.
        """
        if not self.canAdministrateGroup():
            raise Unauthorized, 'You cannot remove a member from the group.'
        self._getGroup().removeMember(id)
        mtool = getToolByName(self, 'portal_membership')
        member = mtool.getMemberById(id)
        if member:
            member.notifyModified()

    removeMember = postonly(removeMember)
    security.declareProtected(Permissions.manage_users, 'setProperties')

    def setProperties(self, properties=None, **kw):
        """Allows the manager group to set his/her own properties.
        Accepts either keyword arguments or a mapping for the "properties"
        argument.
        """
        if properties is None:
            properties = kw
        return self.setGroupProperties(properties)

    security.declareProtected(Permissions.manage_users, 'setGroupProperties')

    def setGroupProperties(self, mapping):
        """Sets the properties of the member.
        """
        tool = self.getTool()
        for id in tool.propertyIds():
            if mapping.has_key(id):
                if not self.__class__.__dict__.has_key(id):
                    value = mapping[id]
                    if type(value) == type(''):
                        proptype = tool.getPropertyType(id) or 'string'
                        if type_converters.has_key(proptype):
                            value = type_converters[proptype](value)
                    setattr(self, id, value)

        self.notifyModified()

    security.declarePublic('getProperties')

    def getProperties(self):
        """ Return the properties of this group. Properties are as usual in Zope."""
        tool = self.getTool()
        ret = {}
        for pty in tool.propertyIds():
            try:
                ret[pty] = self.getProperty(pty)
            except ValueError:
                continue

        return ret

    security.declarePublic('getProperty')

    def getProperty(self, id, default=_marker):
        """ Returns the value of the property specified by 'id' """
        tool = self.getTool()
        base = aq_base(self)
        value = getattr(base, id, _marker)
        if value is not _marker:
            return value
        tool_value = tool.getProperty(id, _marker)
        user_value = getattr(aq_base(self.getGroup()), id, _marker)
        if tool_value is _marker:
            if user_value is not _marker:
                return user_value
            elif default is not _marker:
                return default
            else:
                raise ValueError, 'The property %s does not exist' % id
        if not tool_value and user_value is not _marker:
            return user_value
        return tool_value

    def __str__(self):
        return self.getGroupId()

    security.declarePublic('isGroup')

    def isGroup(self):
        """
        isGroup(self,) => Return true if this is a group.
        Will always return true for groups.
        As MemberData objects do not support this method, it is quite useless by now.
        So one can use groupstool.isGroup(g) instead to get this information.
        """
        return 1

    security.declarePublic('getGroupName')

    def getGroupName(self):
        """Return the name of the group, without any special decorations (like GRUF prefixes.)"""
        return self.getGroup().getName()

    security.declarePublic('getGroupId')

    def getGroupId(self):
        """Get the ID of the group. The ID can be used, at least from
        Python, to get the user from the user's UserDatabase.
        Within Plone, all group ids are UNPREFIXED."""
        if isinstance(self, GRUFGroup):
            return self.getGroup().getId(unprefixed=1)
        else:
            return self.getGroup().getId()

    def getGroupTitleOrName(self):
        """Get the Title property of the group. If there is none
        then return the name """
        title = self.getProperty('title', None)
        return title or self.getGroupName()

    security.declarePublic('getMemberId')

    def getMemberId(self):
        """This exists only for a basic user/group API compatibility
        """
        return self.getGroupId()

    security.declarePublic('getRoles')

    def getRoles(self):
        """Return the list of roles assigned to a user."""
        return self.getGroup().getRoles()

    security.declarePublic('getRolesInContext')

    def getRolesInContext(self, object):
        """Return the list of roles assigned to the user,  including local
        roles assigned in context of the passed in object."""
        return self.getGroup().getRolesInContext(object)

    security.declarePublic('getDomains')

    def getDomains(self):
        """Return the list of domain restrictions for a user"""
        return self.getGroup().getDomains()

    security.declarePublic('has_role')

    def has_role(self, roles, object=None):
        """Check to see if a user has a given role or roles."""
        return self.getGroup().has_role(roles, object)


InitializeClass(GroupData)