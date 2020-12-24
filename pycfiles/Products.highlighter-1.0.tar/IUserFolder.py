# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/interfaces/IUserFolder.py
# Compiled at: 2008-05-20 04:51:54
__doc__ = "\nVOCABULARY:\n\n  - [Pure] User: A user is a user atom who can log itself on, and\n    have additional properties such as domains and password.\n\n  - Group: A group is a user atom other atoms can belong to.\n\n  - User atom: Abstract representation of either a User or\n    a Group.\n\n  - Member (of a group): User atom inside a group.\n\n  - Name (of an atom): For a user, the name can be set by\n    the underlying user folder but usually id == name.\n    For a group, its id is prefixed, but its name is NOT prefixed by 'group_'.\n    For method taking a name instead of an id (eg. getUserByName()),\n    if a user and a group have the same name,\n    the USER will have precedence over the group.\n"
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    from Interface import Base as Interface

class IUserFolder(Interface):
    __module__ = __name__

    def getUserNames():
        """
        Return a list of all possible user atom names in the system.
        Groups will be returned WITHOUT their prefix by this method.
        So, there might be a collision between a user name and a group name.
        [NOTA: This method is time-expensive !]
        """
        pass

    def getUserIds():
        """
        Return a list of all possible user atom ids in the system.
        WARNING: Please see the id Vs. name consideration at the
        top of this document. So, groups will be returned
        WITH their prefix by this method
        [NOTA: This method is time-expensive !]
        """
        pass

    def getUser(name):
        """Return the named user atom object or None
        NOTA: If no user can be found, we try to append a group prefix
        and fetch the user again before returning 'None'. This will ensure
        backward compatibility. So in fact, both group id and group name can be
        specified to this method.
        """
        pass

    def getUsers():
        """Return a list of user atom objects in the users cache.
        In case of some UF implementations, the returned object may only be a subset
        of all possible users.
        In other words, you CANNOT assert that len(getUsers()) equals len(getUserNames()).
        With cache-support UserFolders, such as LDAPUserFolder, the getUser() method will
        return only cached user objects instead of fetching all possible users.
        So this method won't be very time-expensive, but won't be accurate !
        """
        pass

    def getUserById(id, default):
        """Return the user atom corresponding to the given id.
        If default is provided, return default if no user found, else return None.
        """
        pass

    def getUserByName(name, default):
        """Same as getUserById() but works with a name instead of an id.
        If default is provided, return default if no user found, else return None.
        [NOTA: Theorically, the id is a handle, while the name is the actual login name.
        But difference between a user id and a user name is unsignificant in
        all current User Folder implementations... except for GROUPS.]        
        """
        pass

    def hasUsers():
        """
        From Zope 2.7's User.py:
        This is not a formal API method: it is used only to provide
        a way for the quickstart page to determine if the default user
        folder contains any users to provide instructions on how to
        add a user for newbies.  Using getUserNames or getUsers would have
        posed a denial of service risk.
        In GRUF, this method always return 1."""
        pass

    def searchUsersByName(search_term):
        """Return user ids which match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying user folder:
        it may return all users, return only cached users (for LDAPUF) or return no users.
        """
        pass

    def searchUsersById(search_term):
        """Return users whose id match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying user folder:
        it may return all users, return only cached users (for LDAPUF) or return no users.
        """
        pass

    def searchUsersByAttribute(attribute, search_term):
        """Return user ids whose 'attribute' match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying user folder:
        it may return all users, return only cached users (for LDAPUF) or return no users.
        This will return all users whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON USER FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF).
        'attribute' can be 'id' or 'name' for all UF kinds, or anything else for LDAPUF.
        [NOTA: This method is time-expensive !]
        """
        pass

    def searchGroupsByName(search_term):
        """Return group ids which match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying group folder:
        it may return all groups, return only cached groups (for LDAPUF) or return no groups.
        """
        pass

    def searchGroupsById(search_term):
        """Return groups whose id match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying group folder:
        it may return all groups, return only cached groups (for LDAPUF) or return no groups.
        """
        pass

    def searchGroupsByAttribute(attribute, search_term):
        """Return group ids whose 'attribute' match the specified search_term.
        If search_term is an empty string, behaviour depends on the underlying group folder:
        it may return all groups, return only cached groups (for LDAPUF) or return no groups.
        This will return all groups whose name contains search_term (whaterver its case).
        THIS METHOD MAY BE VERY EXPENSIVE ON GROUP FOLDER KINDS WHICH DO NOT PROVIDE A
        SEARCHING METHOD (ie. every UF kind except LDAPUF).
        'attribute' can be 'id' or 'name' for all UF kinds, or anything else for LDAPUF.
        [NOTA: This method is time-expensive !]
        """
        pass

    def getPureUserNames():
        """Same as getUserNames() but without groups
        """
        pass

    def getPureUserIds():
        """Same as getUserIds() but without groups
        """
        pass

    def getPureUsers():
        """Same as getUsers() but without groups.
        """
        pass

    def getPureUser(id):
        """Same as getUser() but forces returning a user and not a group
        """
        pass

    def getGroupNames():
        """Same as getUserNames() but without pure users.
        """
        pass

    def getGroupIds():
        """Same as getUserIds() but without pure users.
        """
        pass

    def getGroups():
        """Same as getUsers() but without pure users.
        In case of some UF implementations, the returned object may only be a subset
        of all possible users.
        In other words, you CANNOT assert that len(getUsers()) equals len(getUserNames()).
        With cache-support UserFolders, such as LDAPUserFolder, the getUser() method will
        return only cached user objects instead of fetching all possible users.
        So this method won't be very time-expensive, but won't be accurate !
        """
        pass

    def getGroup(name):
        """Return the named group object or None. As usual, 'id' is prefixed.
        """
        pass

    def getGroupById(id):
        """Same as getUserById(id) but forces returning a group.
        """
        pass

    def getGroupByName(name):
        """Same as getUserByName(name) but forces returning a group.
        The specified name MUST NOT be prefixed !
        """
        pass

    def userFolderAddUser(name, password, roles, domains, groups, **kw):
        """API method for creating a new user object. Note that not all
        user folder implementations support dynamic creation of user
        objects.
        Groups can be specified by name or by id (preferabily by name)."""
        pass

    def userFolderEditUser(name, password, roles, domains, groups, **kw):
        """API method for changing user object attributes. Note that not
        all user folder implementations support changing of user object
        attributes.
        Groups can be specified by name or by id (preferabily by name)."""
        pass

    def userFolderUpdateUser(name, password, roles, domains, groups, **kw):
        """Same as userFolderEditUser, but with all arguments except name
        being optional.
        """
        pass

    def userFolderDelUsers(names):
        """API method for deleting one or more user atom objects. Note that not
        all user folder implementations support deletion of user objects."""
        pass

    def userFolderAddGroup(name, roles, groups, **kw):
        """API method for creating a new group.
        """
        pass

    def userFolderEditGroup(name, roles, groups, **kw):
        """API method for changing group object attributes.
        """
        pass

    def userFolderUpdateGroup(name, roles, groups, **kw):
        """Same as userFolderEditGroup but with all arguments (except name) being
        optinal.
        """
        pass

    def userFolderDelGroups(names):
        """API method for deleting one or more group objects.
        Implem. note : All ids must be prefixed with 'group_',
        so this method ends up beeing only a filter of non-prefixed ids
        before calling userFolderDelUsers().
        """
        pass

    def userSetRoles(id, roles):
        """Change the roles of a user atom
        """
        pass

    def userAddRole(id, role):
        """Append a role for a user atom
        """
        pass

    def userRemoveRole(id, role):
        """Remove the role of a user atom.
        This will not, of course, affect implicitly-acquired roles from the user groups.
        """
        pass

    def userSetPassword(id, newPassword):
        """Set the password of a user
        """
        pass

    def userSetDomains(id, domains):
        """Set domains for a user
        """
        pass

    def userGetDomains(id):
        """Get domains for a user
        """
        pass

    def userAddDomain(id, domain):
        """Append a domain to a user
        """
        pass

    def userRemoveDomain(id, domain):
        """Remove a domain from a user
        """
        pass

    def userSetGroups(userid, groupnames):
        """Set the groups of a user. Groupnames are, as usual, not prefixed.
        However, a groupid can be given as a fallback
        """
        pass

    def userAddGroup(id, groupname):
        """add a group to a user atom. Groupnames are, as usual, not prefixed.
        However, a groupid can be given as a fallback
        """
        pass

    def userRemoveGroup(id, groupname):
        """remove a group from a user atom. Groupnames are, as usual, not prefixed.
        However, a groupid can be given as a fallback
        """
        pass

    def setRolesOnUsers(roles, userids):
        """Set a common set of roles for a bunch of user atoms.
        """
        pass

    def getUsersOfRole(role, object=None):
        """Gets the user (and group) ids having the specified role...
        ...on the specified Zope object if it's not None
        ...on their own information if the object is None.
        NOTA: THIS METHOD IS VERY EXPENSIVE.
        """
        pass

    def getRolesOfUser(userid):
        """Alias for user.getRoles()
        """
        pass

    def userFolderAddRole(role):
        """Add a new role. The role will be appended, in fact, in GRUF's surrounding folder.
        """
        pass

    def userFolderDelRoles(roles):
        """Delete roles.
        The removed roles will be removed from the UserFolder's users and groups as well,
        so this method can be very time consuming with a large number of users.
        """
        pass

    def userFolderGetRoles():
        """List the roles defined at the top of GRUF's folder.
        """
        pass

    def setMembers(groupid, userids):
        """Set the members of the group
        """
        pass

    def addMember(groupid, id):
        """Add a member to a group
        """
        pass

    def removeMember(groupid, id):
        """Remove a member from a group
        """
        pass

    def hasMember(groupid, id):
        """Return true if the specified atom id is in the group.
        This is the contrary of IUserAtom.isInGroup(groupid).
        THIS CAN BE VERY EXPENSIVE"""
        pass

    def getMemberIds(groupid):
        """Return the list of member ids (groups and users) in this group.
        It will unmangle nested groups as well.
        THIS METHOD CAN BE VERY EXPENSIVE AS IT NEEDS TO FETCH ALL USERS.
        """
        pass

    def getUserMemberIds(groupid):
        """Same as listMemberIds but only return user ids
        THIS METHOD CAN BE VERY EXPENSIVE AS IT NEEDS TO FETCH ALL USERS.
        """
        pass

    def getGroupMemberIds(groupid):
        """Same as listMemberUserIds but only return group ids.
        THIS METHOD CAN BE VERY EXPENSIVE AS IT NEEDS TO FETCH ALL USERS.
        """
        pass

    def acquireLocalRoles(folder, status):
        """Enable or disable local role acquisition on the specified folder.
        If status is true, it will enable, else it will disable.
        """
        pass

    def isLocalRoleAcquired(folder):
        """Return true if the specified folder allows local role acquisition.
        """
        pass

    def getAllLocalRoles(object):
        """getAllLocalRoles(self, object): return a dictionnary {user: roles} of local
        roles defined AND herited at a certain point. This will handle lr-blocking
        as well.
        """
        pass


class IUserAtom(Interface):
    """
    This interface is an abstract representation of what both a User and a Group can do.
    """
    __module__ = __name__

    def getId(unprefixed=0):
        """Get the ID of the user. The ID can be used, at least from
        Python, to get the user from the user's UserDatabase.
        If unprefixed, remove all prefixes in any case."""
        pass

    def getUserName():
        """Alias for getName()
        """
        pass

    def getName():
        """Get user's or group's name.
        For a user, the name can be set by the underlying user folder but usually id == name.
        For a group, the ID is prefixed, but the NAME is NOT prefixed by 'group_'.
        """
        pass

    def getRoles():
        """Return the list of roles assigned to a user atom.
        This will never return gruf-related roles.
        """
        pass

    def getProperty(name):
        """Get a property's value.
        Will raise if not available.
        """
        pass

    def hasProperty(name):
        """Return true if the underlying user object has a value for the property.
        """
        pass

    def setProperty(name, value):
        """Set a property's value.
        As some user folders cannot set properties, this method is not guaranteed to work
        and will raise a NotImplementedError if the underlying user folder cannot store
        properties (or _this_ particular property) for a user.
        """
        pass

    def setRoles(roles):
        """Change user's roles
        """
        pass

    def addRole(role):
        """Append a role to the user
        """
        pass

    def removeRole(role):
        """Remove a role from the user's ones
        """
        pass

    def getRolesInContext(object):
        """Return the list of roles assigned to the user,
           including local roles assigned in context of
           the passed in object."""
        pass

    def has_permission(permission, object):
        """Check to see if a user has a given permission on an object."""
        pass

    def allowed(object, object_roles=None):
        """Check whether the user has access to object. The user must
           have one of the roles in object_roles to allow access."""
        pass

    def has_role(roles, object=None):
        """Check to see if a user has a given role or roles."""
        pass

    def isGroup():
        """Return true if this atom is a group.
        """
        pass

    def getGroupNames():
        """Return the names of the groups that the user or group is directly a member of.
        Return an empty list if the user or group doesn't belong to any group.
        Doesn't include transitive groups."""
        pass

    def getGroupIds():
        """Return the names of the groups that the user or group is a member of.
        Return an empty list if the user or group doesn't belong to any group.
        Doesn't include transitive groups."""
        pass

    def getGroups():
        """getAllGroupIds() alias.
        Return the IDS (not names) of the groups that the user or group is a member of.
        Return an empty list if the user or group doesn't belong to any group.
        THIS WILL INCLUDE TRANSITIVE GROUPS AS WELL."""
        pass

    def getAllGroupIds():
        """Return the names of the groups that the user or group is a member of.
        Return an empty list if the user or group doesn't belong to any group.
        Include transitive groups."""
        pass

    def getAllGroupNames():
        """Return the names of the groups that the user or group is directly a member of.
        Return an empty list if the user or group doesn't belong to any group.
        Include transitive groups."""
        pass

    def isInGroup(groupid):
        """Return true if the user is member of the specified group id
        (including transitive groups)"""
        pass

    def setGroups(groupids):
        """Set 'groupids' groups for the user or group.
        """
        pass

    def addGroup(groupid):
        """Append a group to the current object's groups.
        """
        pass

    def removeGroup(groupid):
        """Remove a group from the object's groups
        """
        pass

    def getRealId():
        """Return group id WITHOUT group prefix.
        For a user, return regular user id.
        This method is essentially internal.
        """
        pass


class IUser(IUserAtom):
    """
    A user is a user atom who can log itself on, and
    have additional properties such as domains and password.
    """
    __module__ = __name__

    def getDomains():
        """Return the list of domain restrictions for a user"""
        pass

    def setPassword(newPassword):
        """Set user's password
        """
        pass

    def setDomains(domains):
        """Replace domains for the user
        """
        pass

    def addDomain(domain):
        """Append a domain for the user
        """
        pass

    def removeDomain(domain):
        """Remove a domain for the user
        """
        pass


class IGroup(Interface):
    """
    A group is a user atom other atoms can belong to.
    """
    __module__ = __name__

    def getMemberIds(transitive=1):
        """Return the member ids (users and groups) of the atoms of this group.
        This method can be very expensive !"""
        pass

    def getUserMemberIds(transitive=1):
        """Return the member ids (users only) of the users of this group"""
        pass

    def getGroupMemberIds(transitive=1):
        """Return the members ids (groups only) of the groups of this group"""
        pass

    def hasMember(id):
        """Return true if the specified atom id is in the group.
        This is the contrary of IUserAtom.isInGroup(groupid)"""
        pass

    def addMember(userid):
        """Add a user the the current group"""
        pass

    def removeMember(userid):
        """Remove a user from the current group"""
        pass