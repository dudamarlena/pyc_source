# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/getpaid/pagseguro/browser/pagsegurobutton.py
# Compiled at: 2009-08-28 18:22:34
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core.interfaces import IShoppingCartUtility, IOrderManager
from getpaid.core.order import Order
from getpaid.core import payment
from cPickle import loads, dumps
from AccessControl import getSecurityManager
from getpaid.pagseguro.pagseguro import PagseguroStandardProcessor

class PagseguroButtonView(BrowserView):
    """page for pagseguro button
    """
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getButton(self):
        button = PagseguroStandardProcessor(self.context)
        cart_util = getUtility(IShoppingCartUtility)
        cart = cart_util.get(self.context, create=True)
        manage_options = IGetPaidManagementOptions(self.context)
        order_manager = getUtility(IOrderManager)
        new_order_id = order_manager.newOrderId()
        order = Order()
        order.processor_id = manage_options.payment_processor
        order.contact_information = payment.ContactInformation()
        order.billing_address = payment.BillingAddress()
        order.shipping_address = payment.ShippingAddress()
        order.order_id = new_order_id
        order.shopping_cart = loads(dumps(cart))
        order.user_id = getSecurityManager().getUser().getId()
        order.finance_workflow.fireTransition('create')
        order_manager.store(order)
        order.finance_workflow.fireTransition('authorize')
        html = button.cart_post_button(order)
        cart_util.destroy(self.context)
        return html