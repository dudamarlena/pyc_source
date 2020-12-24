# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/adapters/shop_management.py
# Compiled at: 2008-09-03 11:15:25
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement

class ShopManagement:
    """Provides IShopManagement for arbitrary objects.
    """
    __module__ = __name__
    implements(IShopManagement)
    adapts(Interface)

    def __init__(self, context):
        """
        """
        self.context = context

    def getShop(self):
        """
        """
        object = self.context
        try:
            while IShop.providedBy(object) == False:
                if object.meta_type == 'Plone Factory Tool':
                    object = object.aq_parent
                else:
                    object = object.aq_inner.aq_parent

        except AttributeError:
            if IShop.providedBy(object.context):
                return object.context
            else:
                return

        return object