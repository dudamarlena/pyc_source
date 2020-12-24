# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/browser/admin/test_environment.py
# Compiled at: 2008-09-03 11:15:24
import random, os
from Globals import package_home
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.config import *
LETTERS = [ chr(i) for i in range(65, 91) ]

class TestEnvironmentView(BrowserView):
    """
    """
    __module__ = __name__

    def createProducts1(self):
        """
        """
        shop = self.context
        categories = []
        for i in range(1, 21):
            id = 'category-%s' % i
            shop.categories.manage_addProduct['easyshop.core'].addCategory(id, title='Category %s' % i)
            category = shop.categories.get(id)
            categories.append(category)
            wftool = getToolByName(self.context, 'portal_workflow')
            wftool.doActionFor(category, 'publish')

        for i in range(1, 101):
            title = self.createTitle()
            id = title.lower()
            shop.products.manage_addProduct['easyshop.core'].addProduct(id, title=title)
            product = shop.products.get(id)
            category = random.choice(categories)
            category.addReference(product, 'categories_products')
            wftool.doActionFor(product, 'publish')

        self.context.portal_catalog.manage_catalogRebuild()

    def createProducts2(self):
        """Add all products to one category.
        """
        shop = self.context
        id = 'category'
        shop.categories.manage_addProduct['easyshop.core'].addCategory(id, title='Category')
        category = shop.categories.get(id)
        wftool = getToolByName(self.context, 'portal_workflow')
        wftool.doActionFor(category, 'publish')
        for i in range(1, 21):
            title = self.createTitle()
            id = title.lower()
            shop.products.manage_addProduct['easyshop.core'].addProduct(id, title=title)
            product = shop.products.get(id)
            img = os.path.join(package_home(globals()), '../../tests/test_2.jpg')
            img = open(img)
            product.setImage(img)
            category.addReference(product, 'categories_products')
            wftool.doActionFor(product, 'publish')

        self.context.portal_catalog.manage_catalogRebuild()

    def createTitle(self):
        """
        """
        return ('').join([ random.choice(LETTERS) for i in range(1, 10) ])

    def setPrices(self):
        """
        """
        from easyshop.core.interfaces import IProductManagement
        base_category = self.context.kategorien['gartenhauser']
        for category in base_category.values():
            if category.id == 'zubehor':
                continue
            for product in IProductManagement(category).getProducts():
                print product
                price = product.getPrice()
                new_price = '%.2f' % (price * 0.95)
                product.setSalePrice(new_price)
                product.setForSale(True)