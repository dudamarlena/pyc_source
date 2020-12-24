# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/interfaces/portal_groupdata.py
# Compiled at: 2008-05-20 04:51:54
__doc__ = 'Groups tool interface\n\nGoes along the lines of portal_memberdata, but for groups.\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
from Interface import Attribute
try:
    from Interface import Interface
except ImportError:
    from Interface import Base as Interface

class portal_groupdata(Interface):
    """ A helper tool for portal_groups that transparently adds
    properties to groups and provides convenience methods"""
    __module__ = __name__

    def wrapGroup(g):
        """ Returns an object implementing the GroupData interface"""
        pass


class GroupData(Interface):
    """ An abstract interface for accessing properties on a group object"""
    __module__ = __name__

    def setProperties(properties=None, **kw):
        """Allows setting of group properties en masse.
        Properties can be given either as a dict or a keyword parameters list"""
        pass

    def getProperty(id):
        """ Return the value of the property specified by 'id' """
        pass

    def getProperties():
        """ Return the properties of this group. Properties are as usual in Zope."""
        pass

    def getGroupId():
        """ Return the string id of this group, WITHOUT group prefix."""
        pass

    def getMemberId():
        """This exists only for a basic user/group API compatibility
        """
        pass

    def getGroupName():
        """ Return the name of the group."""
        pass

    def getGroupMembers():
        """ Return a list of the portal_memberdata-ish members of the group."""
        pass

    def getAllGroupMembers():
        """ Return a list of the portal_memberdata-ish members of the group
        including transitive ones (ie. users or groups of a group in that group)."""
        pass

    def getGroupMemberIds():
        """ Return a list of the user ids of the group."""
        pass

    def getAllGroupMemberIds():
        """ Return a list of the user ids of the group.
        including transitive ones (ie. users or groups of a group in that group)."""
        pass

    def addMember(id):
        """ Add the existing member with the given id to the group"""
        pass

    def removeMember(id):
        """ Remove the member with the provided id from the group """
        pass

    def getGroup():
        """ Returns the actual group implementation. Varies by group
        implementation (GRUF/Nux/et al)."""
        pass