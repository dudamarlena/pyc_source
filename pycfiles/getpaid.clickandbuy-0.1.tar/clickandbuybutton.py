# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/olauzanne/workspace/paguro/getpaid.clickandbuy/getpaid/clickandbuy/browser/clickandbuybutton.py
# Compiled at: 2009-01-30 11:09:25
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager
from getpaid.core.order import Order
from getpaid.core import payment
from cPickle import loads, dumps
from AccessControl import getSecurityManager
from getpaid.clickandbuy.clickandbuy import ClickAndBuyStandardProcessor

class ClickAndBuyButtonView(BrowserView):
    """page for click and buy button
    """
    __module__ = __name__

    def getButton(self):
        button = ClickAndBuyStandardProcessor(self.context)
        cart_util = getUtility(IShoppingCartUtility)
        cart = cart_util.get(self.context, create=True)
        manage_options = IGetPaidManagementOptions(self.context)
        order_manager = getUtility(IOrderManager)
        new_order_id = order_manager.newOrderId()
        order = Order()
        order.finance_workflow.fireTransition('create')
        order.processor_id = manage_options.payment_processor
        order.contact_information = payment.ContactInformation()
        order.billing_address = payment.BillingAddress()
        order.shipping_address = payment.ShippingAddress()
        order.order_id = new_order_id
        order.shopping_cart = loads(dumps(cart))
        order.user_id = getSecurityManager().getUser().getId()
        order_manager.store(order)
        import ipdb
        ipdb.set_trace()
        return button.cart_post_button(order)