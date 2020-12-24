# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/groups/adapters/group_management.py
# Compiled at: 2008-09-03 11:14:50
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IShop

class ShopGroupManagement:
    """An adapter, which provides group management for shop content objects.
    """
    __module__ = __name__
    implements(IGroupManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    def addGroup(self, name):
        """
        """
        putils = getToolByName(self.context, 'plone_utils')
        normalized_id = putils.normalizeString(name)
        if self.getGroup(normalized_id) is None:
            self.context.groups.manage_addProduct['easyshop.core'].addProductGroup(id=normalized_id, title=name)
            return self.getGroup(normalized_id)
        else:
            return False
        return

    def deleteGroup(id):
        """
        """
        raise Exception

    def getGroup(self, group_id):
        """
        """
        return self.context.groups.get(group_id)

    def getGroups(self):
        """Returns all groups
        """
        return self.context.groups.objectValues('ProductGroup')

    def hasGroups():
        """
        """
        raise Exception