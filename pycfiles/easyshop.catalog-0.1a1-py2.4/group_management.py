# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/adapters/group_management.py
# Compiled at: 2008-09-03 11:14:27
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IProduct

class ProductGroupManagement:
    """Provides IGroupManagement for product content objects.
    """
    __module__ = __name__
    implements(IGroupManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context

    def hasGroups(self):
        """
        """
        if len(self.getGroups()) > 0:
            return True
        return False

    def getGroups(self):
        """
        """
        try:
            return self.context.getBRefs('groups_products')
        except AttributeError:
            return []