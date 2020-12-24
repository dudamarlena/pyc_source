# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shipping/browser/shipping_prices.py
# Compiled at: 2008-09-03 11:15:19
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IShopManagement

class ShippingPricesView(BrowserView):
    """
    """
    __module__ = __name__

    def getShippingPrices(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        sm = IShippingPriceManagement(shop)
        cm = ICurrencyManagement(shop)
        result = []
        for shipping_price in sm.getShippingPrices():
            price = cm.priceToString(shipping_price.getPrice())
            result.append({'id': shipping_price.getId(), 'title': shipping_price.Title(), 'description': shipping_price.Description(), 'price': price, 'url': shipping_price.absolute_url(), 'up_url': '%s/es_folder_position?position=up&id=%s' % (self.context.absolute_url(), shipping_price.getId()), 'down_url': '%s/es_folder_position?position=down&id=%s' % (self.context.absolute_url(), shipping_price.getId()), 'amount_of_criteria': self._getAmountOfCriteria(shipping_price.getId())})

        return result

    def _getAmountOfCriteria(self, id):
        """Returns amount of criteria for tax with given id.
        """
        try:
            tax = self.context[id]
        except KeyError:
            return 0

        return len(tax.objectIds())