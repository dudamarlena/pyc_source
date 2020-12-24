# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_product_group.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IGroupManagement

class TestProductGroupManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestProductGroupManagement, self).afterSetUp()
        self.shop.products.invokeFactory('Product', id='product_3', price=19.0)
        self.product_3 = self.shop.products.product_3

    def testHasGroups(self):
        """
        """
        cm = IGroupManagement(self.shop.products.product_1)
        self.assertEqual(cm.hasGroups(), True)
        cm = IGroupManagement(self.shop.products.product_3)
        self.assertEqual(cm.hasGroups(), False)

    def testGetGroups_1(self):
        """
        """
        cm = IGroupManagement(self.shop.products.product_1)
        ids = [ g.getId() for g in cm.getGroups() ]
        self.assertEqual(ids, ['group_1', 'group_2'])

    def testGetGroups_2(self):
        """
        """
        cm = IGroupManagement(self.shop.products.product_3)
        self.assertEqual(cm.getGroups(), [])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductGroupManagement))
    return suite