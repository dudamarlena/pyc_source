# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/groups.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface
from zope.interface import Attribute

class IProductGroup(Interface):
    """A group combines arbitrary products.
    o Groups may then assigned special taxes, shipping prices, discounts and 
      similiar.
    o As a specialty groups may have assigned properties. All products, which 
      are within a group inherit properties of this group.
    o Groups are in contrary to categories not visible to customers.
    """
    __module__ = __name__
    products = Attribute('Products which belongs to this group.')


class IGroupManagement(Interface):
    """Provides methods to manage groups.
    """
    __module__ = __name__

    def addGroup(group):
        """Adds given group.
        """
        pass

    def deleteGroup(id):
        """Deletes group with given id.
        """
        pass

    def getGroup(group_id):
        """Returns a group by given id.
        """
        pass

    def getGroups():
        """Returns all Groups
        """
        pass

    def hasGroups():
        """Returns True, if there is at least on Group.
        """
        pass


class IGroupsContainer(Interface):
    """A container to hold groups.
    """
    __module__ = __name__