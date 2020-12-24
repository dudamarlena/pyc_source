# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_discounts_management.py
# Compiled at: 2008-06-20 09:37:19
from base import EasyShopTestCase
from easyshop.core.interfaces import IDiscountsManagement

class TestDiscountsManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestDiscountsManagement, self).afterSetUp()

    def testGetDiscounts1(self):
        """There are no discounts.
        """
        dm = IDiscountsManagement(self.shop)
        self.assertEqual(dm.getDiscounts(), [])

    def testGetDiscounts2(self):
        """
        """
        self.shop.discounts.invokeFactory('Discount', id='d1', title='D1', value='1.0')
        self.shop.discounts.invokeFactory('Discount', id='d2', title='D2', value='2.0', base='cart_item', type='percentage')
        dm = IDiscountsManagement(self.shop)
        discount = dm.getDiscounts()[0]
        self.assertEqual(discount.getId(), 'd1')
        self.assertEqual(discount.Title(), 'D1')
        self.assertEqual(discount.getValue(), 1.0)
        self.assertEqual(discount.getBase(), 'product')
        self.assertEqual(discount.getType(), 'absolute')
        discount = dm.getDiscounts()[1]
        self.assertEqual(discount.getId(), 'd2')
        self.assertEqual(discount.Title(), 'D2')
        self.assertEqual(discount.getValue(), 2.0)
        self.assertEqual(discount.getBase(), 'cart_item')
        self.assertEqual(discount.getType(), 'percentage')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDiscountsManagement))
    return suite