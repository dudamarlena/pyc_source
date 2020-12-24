# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/discounts/adapters/discounts_management.py
# Compiled at: 2008-09-03 11:14:47
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IDiscountsManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IValidity

class DiscountsManagement:
    """An adapter which provides IDiscountsManagement for shop content objects.
    """
    __module__ = __name__
    implements(IDiscountsManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.discounts = self.context.discounts

    def getDiscounts(self):
        """Returns all existing discounts.
        """
        return self.discounts.objectValues()