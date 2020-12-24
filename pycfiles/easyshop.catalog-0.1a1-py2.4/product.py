# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/viewlets/product.py
# Compiled at: 2008-09-03 11:14:26
from zope.component import queryUtility
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from easyshop.core.config import _
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class ProductViewlet(ViewletBase):
    """
    """
    __module__ = __name__
    render = ViewPageTemplateFile('product.pt')

    def getBuyLabel(self):
        """
        """
        pm = IPropertyManagement(self.context)
        if len(pm.getProperties()) > 0:
            return 'Buy Product'
        else:
            return 'Add to Cart'

    def getPriceForCustomer(self):
        """
        """
        p = IPrices(self.context)
        price = p.getPriceForCustomer()
        if IProductVariantsManagement(self.context).hasVariants() == False:
            total_diff = 0.0
            pm = IPropertyManagement(self.context)
            for (property_id, selected_option) in self.request.form.items():
                if property_id.startswith('property'):
                    total_diff += pm.getPriceForCustomer(property_id[9:], selected_option)

            price += total_diff
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)

    def getStandardPriceForCustomer(self):
        """Returns the standard price for a customer when the product is for 
        sale. Used to display the crossed-out standard price.
        """
        p = IPrices(self.context)
        price = p.getPriceForCustomer(effective=False)
        if IProductVariantsManagement(self.context).hasVariants() == False:
            total_diff = 0.0
            pm = IPropertyManagement(self.context)
            for (property_id, selected_option) in self.request.form.items():
                if property_id.startswith('property'):
                    total_diff += pm.getPriceForCustomer(property_id[9:], selected_option)

            price + total_diff
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)

    def getProductData(self):
        """
        """
        data = IData(self.context)
        return data.asDict()

    def getImageUrls(self):
        """
        """
        pm = IImageManagement(self.context)
        result = []
        for image in pm.getImages():
            result.append('%s/image_tile' % image.absolute_url())

        return result

    def getProperties(self):
        """
        """
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants():
            return self._getPropertiesForVariants()
        else:
            return self._getPropertiesForConfiguration()

    def _getPropertiesForConfiguration(self):
        """
        """
        u = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
        selected_options = {}
        for (name, value) in self.request.items():
            if name.startswith('property'):
                selected_options[name[9:]] = value

        pm = IPropertyManagement(self.context)
        result = []
        for property in pm.getProperties():
            if len(property.getOptions()) == 0:
                continue
            options = [{'id': 'select', 'title': _('Select'), 'selected': False}]
            for option in property.getOptions():
                option_id = option['id']
                option_name = option['name']
                option_price = option['price']
                if option_price != '0.0':
                    option_price = u.stringToFloat(option_price)
                    option_price = cm.priceToString(option_price, 'long', 'after')
                    content = '%s %s' % (option_name, option_price)
                else:
                    content = option_name
                selected_option = selected_options.get(property.getId(), '')
                selected = option_id == selected_option
                options.append({'id': option_id, 'title': content, 'selected': selected})

            result.append({'id': 'property_' + property.getId(), 'title': property.Title(), 'options': options})

        return result

    def _getPropertiesForVariants(self):
        """
        """
        u = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
        selected_options = {}
        for (name, value) in self.request.items():
            if name.startswith('property'):
                selected_options[name[9:]] = value

        if selected_options == {}:
            pvm = IProductVariantsManagement(self.context)
            default_variant = pvm.getDefaultVariant()
            if default_variant is None:
                return []
            for property in default_variant.getForProperties():
                (name, value) = property.split(':')
                selected_options[name] = value

        pm = IPropertyManagement(self.context)
        result = []
        for property in pm.getProperties():
            if len(property.getOptions()) == 0:
                continue
            options = []
            for option in property.getOptions():
                option_id = option['id']
                option_name = option['name']
                content = option_name
                selected_option = selected_options.get(property.getId(), '')
                selected = option_id == selected_option
                options.append({'id': option_id, 'title': content, 'selected': selected})

            result.append({'id': 'property_' + property.getId(), 'title': property.Title(), 'options': options})

        return result

    def getRelatedProducts(self):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        result = []
        for product in self.context.getRefs('products_products'):
            if mtool.checkPermission('View', product) is not None:
                result.append(product)

        return result

    def getStockInformation(self):
        """
        """
        shop = self._getShop()
        sm = IStockManagement(shop)
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants() == False:
            stock_information = sm.getStockInformationFor(self.context)
        else:
            product_variant = pvm.getSelectedVariant()
            stock_information = sm.getStockInformationFor(product_variant)
            if stock_information is None:
                stock_information = sm.getStockInformationFor(self.context)
        if stock_information is None:
            return
        return IData(stock_information).asDict()

    def showAddQuantity(self):
        """
        """
        shop = self._getShop()
        return shop.getShowAddQuantity()

    @memoize
    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()