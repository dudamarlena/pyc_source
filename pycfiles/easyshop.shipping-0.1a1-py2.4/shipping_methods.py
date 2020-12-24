# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shipping/browser/shipping_methods.py
# Compiled at: 2008-09-03 11:15:19
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShopManagement

class ShippingMethodsView(BrowserView):
    """
    """
    __module__ = __name__

    def getShippingMethods(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        pm = IShippingMethodManagement(shop)
        result = []
        for shipping_method in pm.getShippingMethods():
            result.append({'id': shipping_method.getId(), 'title': shipping_method.Title(), 'url': shipping_method.absolute_url(), 'up_url': '%s/es_folder_position?position=up&id=%s' % (self.context.absolute_url(), shipping_method.getId()), 'down_url': '%s/es_folder_position?position=down&id=%s' % (self.context.absolute_url(), shipping_method.getId()), 'amount_of_criteria': self._getAmountOfCriteria(shipping_method.getId())})

        return result

    def _getAmountOfCriteria(self, id):
        """Returns amount of criteria for tax with given id.
        """
        try:
            method = self.context[id]
        except KeyError:
            return 0

        return len(method.objectIds())