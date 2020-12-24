# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/order/browser/orders.py
# Compiled at: 2008-09-03 11:15:08
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IShopManagement

class OrdersView(BrowserView):
    """
    """
    __module__ = __name__

    def getOrders(self):
        """
        """
        tool = getToolByName(self.context, 'translation_service')
        shop = IShopManagement(self.context).getShop()
        wftool = getToolByName(self.context, 'portal_workflow')
        filter = self.request.get('filter', 'all')
        if filter == 'all':
            filter = None
        sorting = self.request.get('sorting', 'created')
        order = self.request.get('order', 'descending')
        orders = []
        om = IOrderManagement(shop)
        for order in om.getOrders(filter, sorting, order):
            fullname = 'There is no customer.'
            customer = order.getCustomer()
            if customer is not None:
                am = IAddressManagement(customer)
                address = am.getInvoiceAddress()
                if address is not None:
                    fullname = address.getName(reverse=True)
            created = tool.ulocalized_time(order.created(), long_format=True)
            orders.append({'id': order.getId(), 'url': order.absolute_url(), 'created': created, 'customer_name': fullname, 'review_state': wftool.getInfoFor(order, 'review_state')})

        return orders