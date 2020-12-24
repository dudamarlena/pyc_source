# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/browser/payment_prices.py
# Compiled at: 2008-09-03 11:15:13
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IShopManagement

class PaymentPricesView(BrowserView):
    """
    """
    __module__ = __name__

    def getPaymentPrices(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        pp = IPaymentPriceManagement(shop)
        cm = ICurrencyManagement(shop)
        result = []
        for payment_price in pp.getPaymentPrices():
            price = cm.priceToString(payment_price.getPrice())
            result.append({'id': payment_price.getId(), 'title': payment_price.Title(), 'price': price, 'url': payment_price.absolute_url(), 'up_url': '%s/es_folder_position?position=up&id=%s' % (self.context.absolute_url(), payment_price.getId()), 'down_url': '%s/es_folder_position?position=down&id=%s' % (self.context.absolute_url(), payment_price.getId()), 'amount_of_criteria': self._getAmountOfCriteria(payment_price.getId())})

        return result

    def _getAmountOfCriteria(self, id):
        """Returns amount of criteria for tax with given id.
        """
        try:
            tax = self.context[id]
        except KeyError:
            return 0

        return len(tax.objectIds())