# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_product_category.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICategoryManagement

class TestProductCategoryManager(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestProductCategoryManager, self).afterSetUp()
        self.shop.products.invokeFactory('Product', id='product_3', price=19.0)
        self.product_3 = self.shop.products.product_3

    def testGetTopLevelCategories_1(self):
        """
        """
        cm = ICategoryManagement(self.product_1)
        ids = [ c.getId() for c in cm.getTopLevelCategories() ]
        self.assertEqual(ids, ['category_11'])
        self.shop.categories.invokeFactory('Category', id='category_a')
        self.shop.categories.invokeFactory('Category', id='category_b')
        self.shop.categories.category_a.addReference(self.product_1, 'categories_products')
        self.shop.categories.category_b.addReference(self.product_1, 'categories_products')
        ids = [ c.getId() for c in cm.getTopLevelCategories() ]
        self.failUnless(len(ids) == 3)
        for id in ['category_11', 'category_a', 'category_b']:
            self.failUnless(id in ids)

    def testGetTopLevelCategories_2(self):
        """No categories there
        """
        cm = ICategoryManagement(self.product_3)
        self.assertEqual(cm.getTopLevelCategories(), [])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductCategoryManager))
    return suite