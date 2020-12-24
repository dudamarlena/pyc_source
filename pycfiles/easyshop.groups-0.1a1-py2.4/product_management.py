# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/groups/adapters/product_management.py
# Compiled at: 2008-09-03 11:14:50
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IProductGroup

class GroupProductManager:
    """
    """
    __module__ = __name__
    implements(IProductManagement)
    adapts(IProductGroup)

    def __init__(self, context):
        """
        """
        self.context = context

    def getProducts(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        result = []
        for product in self.context.getRefs('groups_products'):
            if mtool.checkPermission('View', product) is not None:
                result.append(product)

        return result

    def getAmountOfProducts(self):
        """
        """
        return len(self.getProducts())