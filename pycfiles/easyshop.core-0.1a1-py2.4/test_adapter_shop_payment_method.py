# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_shop_payment_method.py
# Compiled at: 2008-06-20 09:37:19
from base import EasyShopTestCase
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IPaymentPriceManagement

class TestPaymentMethodManagement(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestPaymentMethodManagement, self).afterSetUp()
        self.shop.customers.invokeFactory('Customer', 'customer')
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()

    def testDeletePaymentMethod(self):
        """
        """
        pm = IPaymentMethodManagement(self.shop)
        ids = [ p.getId() for p in pm.getPaymentMethods() ]
        self.assertEqual(['cash-on-delivery', 'credit-card', 'direct-debit', 'paypal', 'prepayment'], ids)
        result = pm.deletePaymentMethod('paypal')
        self.assertEqual(result, True)
        ids = [ p.getId() for p in pm.getPaymentMethods() ]
        self.assertEqual(['cash-on-delivery', 'credit-card', 'direct-debit', 'prepayment'], ids)
        result = pm.deletePaymentMethod('prepayment')
        self.assertEqual(result, True)
        ids = [ p.getId() for p in pm.getPaymentMethods() ]
        self.assertEqual(['cash-on-delivery', 'credit-card', 'direct-debit'], ids)
        result = pm.deletePaymentMethod('direct-debit')
        self.assertEqual(result, True)
        ids = [ p.getId() for p in pm.getPaymentMethods() ]
        self.assertEqual(['cash-on-delivery', 'credit-card'], ids)
        result = pm.deletePaymentMethod('paypal')
        self.assertEqual(result, False)
        result = pm.deletePaymentMethod('prepayment')
        self.assertEqual(result, False)

    def testGetPaymentMethods(self):
        """Get all payment methods (without parameter)
        """
        pm = IPaymentMethodManagement(self.shop)
        ids = [ p.getId() for p in pm.getPaymentMethods() ]
        self.assertEqual(['cash-on-delivery', 'credit-card', 'direct-debit', 'paypal', 'prepayment'], ids)


class TestPaymentPrices(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestPaymentPrices, self).afterSetUp()
        self.shop.customers.invokeFactory('Customer', 'customer')
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()

    def testGetPaymentPrices(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        ids = [ pp.getId() for pp in pp.getPaymentPrices() ]
        self.assertEqual(ids, ['default'])

    def testGetPriceGross(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        price_gross = pp.getPriceGross()
        self.assertEqual(price_gross, 100.0)

    def testGetPriceForCustomer(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        price_gross = pp.getPriceGross()
        self.assertEqual(price_gross, 100.0)

    def testGetPriceNet(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        price_net = pp.getPriceNet()
        self.assertEqual('%.2f' % price_net, '84.03')

    def testGetTax(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        tax = pp.getTax()
        self.assertEqual('%.2f' % tax, '15.97')

    def testGetTaxForCustomer(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        tax = pp.getTaxForCustomer()
        self.assertEqual('%.2f' % tax, '15.97')

    def testGetTaxRate(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        tax = pp.getTaxRate()
        self.assertEqual(tax, 19.0)

    def testGetTaxRateForCustomer(self):
        """
        """
        pp = IPaymentPriceManagement(self.shop)
        tax = pp.getTaxRateForCustomer()
        self.assertEqual(tax, 19.0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaymentMethodManagement))
    suite.addTest(makeSuite(TestPaymentPrices))
    return suite