# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_category.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICategoryManagement

class TestShopCategoryManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def testGetCategories(self):
        """
        """
        cm = ICategoryManagement(self.shop)
        ids = [ c.id for c in cm.getCategories() ]
        self.failUnless('category_1' in ids)
        self.failUnless('category_2' in ids)
        self.failUnless('category_11' in ids)
        self.failUnless('category_111' in ids)

    def testGetTopLevelCategories(self):
        """
        """
        cm = ICategoryManagement(self.shop)
        ids = [ c.id for c in cm.getTopLevelCategories() ]
        self.assertEqual(ids, ['category_1', 'category_2', 'category_3'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopCategoryManagement))
    return suite