# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/order/browser/my_orders.py
# Compiled at: 2008-09-03 11:15:08
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IShopManagement

class MyOrdersView(BrowserView):
    """
    """
    __module__ = __name__

    def getOrders(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        om = IOrderManagement(shop)
        orders = om.getOrdersForAuthenticatedCustomer()
        wftool = getToolByName(self.context, 'portal_workflow')
        ttool = getToolByName(self.context, 'translation_service')
        result = []
        for order in orders:
            order_view = getMultiAdapter((order, self.request), name='order')
            created = ttool.ulocalized_time(order.created(), long_format=True)
            temp = {'id': order.getId(), 'url': order.absolute_url(), 'price_gross': order_view.getPriceForCustomer(), 'shipping': order_view.getShipping(), 'payment': order_view.getPaymentValues(), 'items_': order_view.getItems(), 'creation_date': created, 'state': wftool.getInfoFor(order, 'review_state'), 'tax': order_view.getTax()}
            result.append(temp)

        return result