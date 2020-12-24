# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shipping/content/shipping_price.py
# Compiled at: 2008-09-03 11:15:19
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IShippingPrice
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement

class ShippingPriceBase(OrderedBaseFolder):
    """The base class for shipping prices. Developer may inherit from it, to 
    write own shipping prices.
    """
    __module__ = __name__
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseFolderSchema.copy()

    def getCart(self):
        """Provides the cart of authenticated customer.
        """
        shop = IShopManagement(self).getShop()
        return ICartManagement(shop).getCart()

    def getCartItems(self):
        """Provides the cart items.
        """
        cart = self.getCart()
        return IItemManagement(cart).getItems()


schema = Schema((FloatField(name='price', widget=DecimalWidget(size='10', label='Price', label_msgid='schema_price_label', i18n_domain='EasyShop')),))
schema = OrderedBaseFolder.schema.copy() + schema
schema['description'].schemata = 'default'

class ShippingPrice(ShippingPriceBase):
    """Represents a price for shipping. Has criteria which makes it possible
    for the Shipping manager to calculate a shipping price.
    """
    __module__ = __name__
    implements(IShippingPrice)
    schema = schema


registerType(ShippingPrice, PROJECTNAME)