# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/adapters/product_management.py
# Compiled at: 2008-09-03 11:14:27
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShop

class CategoryProductManagement(object):
    """An adapter which provides IProductManagement for category content
    objects.
    """
    __module__ = __name__
    implements(IProductManagement)
    adapts(ICategory)

    def __init__(self, context):
        """
        """
        self.context = context

    def getProducts(self, category_id=None):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        result = []
        for product in self.context.getRefs('categories_products'):
            if mtool.checkPermission('View', product) is not None:
                result.append(product)

        return result

    def getAllProducts(self, sorted_on=None, sort_order=None):
        """
        """
        pm = IProductManagement(self.context)
        products = pm.getProducts()
        cm = ICategoryManagement(self.context)
        for category in cm.getCategories():
            pm = IProductManagement(category)
            products.extend(pm.getProducts())

        if sorted_on == 'name':
            products = self._sortProductsByName(products, sort_order)
        elif sorted_on == 'price':
            products = self._sortProductsByPrice(products, sort_order)
        return products

    def getAmountOfProducts(self):
        """
        """
        return len(self.getProducts())

    def getTotalAmountOfProducts(self):
        """
        """
        return len(self.getAllProducts())

    def _sortProductsByName(self, products, order=None):
        """Sorts given products by name.
        """
        if order == 'desc':
            products.sort(lambda a, b: cmp(b.Title(), a.Title()))
        else:
            products.sort(lambda a, b: cmp(a.Title(), b.Title()))
        return products

    def _sortProductsByPrice(self, products, order=None):
        """Sorts given products by price.
        """
        if order == 'desc':
            products.sort(lambda a, b: cmp(IPrices(b).getPriceGross(), IPrices(a).getPriceGross()))
        else:
            products.sort(lambda a, b: cmp(IPrices(a).getPriceGross(), IPrices(b).getPriceGross()))
        return products


class ShopProductManagement(object):
    """An adapter which provides IProductManagement for shop content objects.
    """
    __module__ = __name__
    implements(IProductManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    def getAllProducts(self):
        """
        """
        raise Exception

    def getAmountOfProducts(self):
        """
        """
        raise Exception

    def getProducts(self):
        """
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(portal_type='Product', path=('/').join(self.context.getPhysicalPath()), sort_on='sortable_title')
        return brains

    def getTotalAmountOfProducts(self):
        """
        """
        raise Exception