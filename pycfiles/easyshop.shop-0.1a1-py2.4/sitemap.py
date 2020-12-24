# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/browser/sitemap.py
# Compiled at: 2008-09-03 11:15:24
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductManagement

class SitemapView(BrowserView):
    """
    """
    __module__ = __name__

    def getCategories(self):
        """
        """
        shop = self._getShop()
        categories = ICategoryManagement(shop).getTopLevelCategories()
        result = []
        for category in categories:
            klass = ''
            if self._isCurrentItem(category) == True:
                klass += 'navTreeCurrentItem'
            result.append({'klass': klass, 'url': category.getURL, 'description': category.Description, 'title': category.Title, 'amount_of_products': category.total_amount_of_products, 'subcategories': self._getSubCategories(category), 'products': self._getProducts(category)})

        return result

    def getShopUrl(self):
        """
        """
        utool = getToolByName(self.context, 'portal_url')
        portal = utool.getPortalObject()
        props = getToolByName(self.context, 'portal_properties').site_properties
        shop_path = props.easyshop_path
        return portal.absolute_url() + shop_path

    def _getSubCategories(self, category):
        """
        """
        result = []
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(portal_type='Category', path={'query': category.getPath(), 'depth': 1}, sort_on='getObjPositionInParent')
        for category in brains:
            klass = ''
            if self._isCurrentItem(category) == True:
                klass += 'navTreeCurrentItem'
            result.append({'klass': klass, 'url': category.getURL, 'description': category.Description, 'title': category.Title, 'amount_of_products': category.total_amount_of_products, 'subcategories': self._getSubCategories(category), 'products': self._getProducts(category)})

        return result

    def _getProducts(self, category):
        """
        """
        object = category.getObject()
        products = []
        for product in IProductManagement(object).getProducts():
            products.append({'title': product.Title(), 'url': product.absolute_url()})

        return products

    def _isCurrentItem(self, category):
        """Selected category and parent are current categories.
        """
        context_url = self.context.absolute_url()
        category_url = category.getURL()
        if context_url.startswith(category_url):
            return True
        elif IProduct.providedBy(self.context):
            try:
                product_category = self.context.getBRefs('categories_products')[0]
            except IndexError:
                return False
            else:
                category_url = category.getPath()
                context_url = ('/').join(product_category.getPhysicalPath())
                if context_url.startswith(category_url):
                    return True
        return False

    @memoize
    def _getShop(self):
        """
        """
        props = getToolByName(self.context, 'portal_properties').site_properties
        shop_path = props.easyshop_path
        utool = getToolByName(self.context, 'portal_url')
        portal = utool.getPortalObject()
        shop = portal.restrictedTraverse(shop_path)
        return shop