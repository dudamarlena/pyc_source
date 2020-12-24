# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_stockinformation_data.py
# Compiled at: 2008-06-20 09:37:19
from base import EasyShopTestCase
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IStockManagement

class TestStockInformationData(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestStockInformationData, self).afterSetUp()
        container = self.shop['stock-information']
        container.invokeFactory('StockInformation', id='s1')
        sm = IStockManagement(self.shop)
        self.si = sm.getStockInformationFor(self.shop.products.product_1)

    def testAsDict1(self):
        """
        """
        self.si.setDeliveryTimeMin('1')
        self.si.setDeliveryTimeMax('2')
        self.si.setDeliveryTimeUnit('Days')
        data = IData(self.si).asDict()
        self.assertEqual(data['time_period'], '1-2')
        self.assertEqual(data['time_unit'], 'Days')

    def testAsDict2(self):
        """
        """
        self.si.setDeliveryTimeMin('2')
        self.si.setDeliveryTimeMax('2')
        self.si.setDeliveryTimeUnit('Days')
        data = IData(self.si).asDict()
        self.assertEqual(data['time_period'], '2')
        self.assertEqual(data['time_unit'], 'Days')

    def testAsDict3(self):
        """
        """
        self.si.setDeliveryTimeMin('1')
        self.si.setDeliveryTimeMax('1')
        self.si.setDeliveryTimeUnit('Days')
        data = IData(self.si).asDict()
        self.assertEqual(data['time_period'], '1')
        self.assertEqual(data['time_unit'], 'Day')

    def testAsDict4(self):
        """
        """
        self.si.setDeliveryTimeMin('1')
        self.si.setDeliveryTimeMax('1')
        self.si.setDeliveryTimeUnit('Weeks')
        data = IData(self.si).asDict()
        self.assertEqual(data['time_period'], '1')
        self.assertEqual(data['time_unit'], 'Week')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStockInformationData))
    return suite