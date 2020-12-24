# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/interfaces/portal_groups.py
# Compiled at: 2008-05-20 04:51:54
"""Groups tool interface

Goes along the lines of portal_membership, but for groups.
"""
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    from Interface import Base as Interface

class portal_groups(Interface):
    """Defines an interface for working with groups in an abstract manner.
    Parallels the portal_membership interface of CMFCore"""
    __module__ = __name__

    def isGroup(u):
        """Test if a user/group object is a group or not.
        You must pass an object you get earlier with wrapUser() or wrapGroup()
        """
        pass

    def getGroupById(id):
        """Returns the portal_groupdata-ish object for a group corresponding
        to this id."""
        pass

    def getGroupsByUserId(userid):
        """Returns a list of the groups the user corresponding to 'userid' belongs to."""
        pass

    def listGroups():
        """Returns a list of the available portal_groupdata-ish objects."""
        pass

    def listGroupIds():
        """Returns a list of the available groups' ids (WITHOUT prefixes)."""
        pass

    def listGroupNames():
        """Returns a list of the available groups' names (ie. without prefixes)."""
        pass

    def searchForGroups(REQUEST, **kw):
        """Return a list of groups meeting certain conditions. """
        pass

    def addGroup(id, roles=[], groups=[], **kw):
        """Create a group with the supplied id, roles, and groups.

        Underlying user folder must support adding users via the usual Zope API.
        Passwords for groups seem to be currently irrelevant in GRUF."""
        pass

    def editGroup(id, roles=[], groups=[], **kw):
        """Edit the given group with the supplied roles.

        Underlying user folder must support editing users via the usual Zope API.
        Passwords for groups seem to be currently irrelevant in GRUF.
        One can supply additional named parameters to set group properties."""
        pass

    def removeGroups(ids, keep_workspaces=0):
        """Remove the group in the provided list (if possible).

        Will by default remove this group's GroupWorkspace if it exists. You may
        turn this off by specifying keep_workspaces=true.
        Underlying user folder must support removing users via the usual Zope API."""
        pass

    def setGroupOwnership(group, object):
        """Make the object 'object' owned by group 'group' (a portal_groupdata-ish object)"""
        pass

    def setGroupWorkspacesFolder(id=''):
        """ Set the location of the Group Workspaces folder by id.

        The Group Workspaces Folder contains all the group workspaces, just like the
        Members folder contains all the member folders.

        If anyone really cares, we can probably make the id work as a path as well,
        but for the moment it's only an id for a folder in the portal root, just like the
        corresponding MembershipTool functionality. """
        pass

    def getGroupWorkspacesFolderId():
        """ Get the Group Workspaces folder object's id.

        The Group Workspaces Folder contains all the group workspaces, just like the
        Members folder contains all the member folders. """
        pass

    def getGroupWorkspacesFolder():
        """ Get the Group Workspaces folder object.

        The Group Workspaces Folder contains all the group workspaces, just like the
        Members folder contains all the member folders. """
        pass

    def toggleGroupWorkspacesCreation():
        """ Toggles the flag for creation of a GroupWorkspaces folder upon first
        use of the group. """
        pass

    def getGroupWorkspacesCreationFlag():
        """Return the (boolean) flag indicating whether the Groups Tool will create a group workspace
        upon the next use of the group (if one doesn't exist). """
        pass

    def getGroupWorkspaceType():
        """Return the Type (as in TypesTool) to make the GroupWorkspace."""
        pass

    def setGroupWorkspaceType(type):
        """Set the Type (as in TypesTool) to make the GroupWorkspace. Expects the name of a Type."""
        pass

    def createGrouparea(id):
        """Create a space in the portal for the given group, much like member home
        folders."""
        pass

    def getGroupareaFolder(id):
        """Returns the object of the group's work area."""
        pass

    def getGroupareaURL(id):
        """Returns the full URL to the group's work area."""
        pass