# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/browser/add_to_cart.py
# Compiled at: 2008-09-03 11:14:28
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement

class ProductAddToCartView(BrowserView):
    """
    """
    __module__ = __name__

    def addToCart(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        cm = ICartManagement(shop)
        cart = cm.getCart()
        if cart is None:
            cart = cm.createCart()
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants():
            product = pvm.getSelectedVariant() or pvm.getDefaultVariant()
            properties = []
            for property in product.getForProperties():
                (property_id, selected_option) = property.split(':')
                properties.append({'id': property_id, 'selected_option': selected_option})

        else:
            product = self.context
            properties = []
            for property in IPropertyManagement(product).getProperties():
                selected_option_id = self.request.get('property_%s' % property.getId())
                if selected_option_id is None or selected_option_id == 'select':
                    property = IPropertyManagement(product).getProperty(property.getId())
                    selected_option = property.getOptions()[0]
                    selected_option_id = selected_option['id']
                properties.append({'id': property.getId(), 'selected_option': selected_option_id})

            quantity = int(self.context.request.get('quantity', 1))
            (result, item_id) = IItemManagement(cart).addItem(product, tuple(properties), quantity)
            putils = getToolByName(self.context, 'plone_utils')
            if result == True:
                putils.addPortalMessage(MESSAGES['CART_INCREASED_AMOUNT'])
            else:
                putils.addPortalMessage(MESSAGES['CART_ADDED_PRODUCT'])
        url = '%s/added-to-cart?id=%s' % (shop.absolute_url(), item_id)
        self.context.request.response.redirect(url)
        return