# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/order/subscribers/mailing.py
# Compiled at: 2008-09-03 11:15:08
from zope.component import adapter
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IMailAddresses
from easyshop.core.interfaces import IOrder
from easyshop.core.interfaces import IShopManagement
from easyshop.shop.utilities.misc import sendMultipartMail

@adapter(IOrder, IAfterTransitionEvent)
def sendOrderMail(order, event):
    """
    """
    state = event.new_state.getId()
    if state == 'pending':
        mailOrderSubmitted(order)
        mailOrderReceived(order)
    elif state in ('sent (not payed)', 'sent'):
        mailOrderSent(order)


def mailOrderSent(order):
    """Sends email to customer that the order has been sent.
    """
    shop = IShopManagement(order).getShop()
    view = getMultiAdapter((order, order.REQUEST), name='mail-order-sent')
    text = view()
    customer = order.getCustomer()
    props = getToolByName(order, 'portal_properties').site_properties
    charset = props.getProperty('default_charset')
    sender = IMailAddresses(shop).getSender()
    sendMultipartMail(context=order, sender=sender, receiver=customer.email, subject='Your order %s has been sent.' % order.getId(), text=text, charset=charset)


def mailOrderSubmitted(order):
    """Sends email to shop owner that an order has been submitted.
    """
    shop = IShopManagement(order).getShop()
    mail_addresses = IMailAddresses(shop)
    sender = mail_addresses.getSender()
    receivers = mail_addresses.getReceivers()
    if sender and receivers:
        view = getMultiAdapter((order, order.REQUEST), name='mail-order-submitted')
        text = view()
        props = getToolByName(order, 'portal_properties').site_properties
        charset = props.getProperty('default_charset')
        sendMultipartMail(context=order, sender=sender, receiver=(', ').join(receivers), subject='E-Shop: New order', text=text, charset=charset)


def mailOrderReceived(order):
    """Sends email to customer that the order has been received.
    """
    shop = IShopManagement(order).getShop()
    mail_addresses = IMailAddresses(shop)
    sender = mail_addresses.getSender()
    bcc = mail_addresses.getReceivers()
    customer = order.getCustomer()
    address = IAddressManagement(customer).getShippingAddress()
    receiver = address.email
    if sender and receiver:
        view = getMultiAdapter((order, order.REQUEST), name='mail-order-received')
        text = view()
        props = getToolByName(order, 'portal_properties').site_properties
        charset = props.getProperty('default_charset')
        sendMultipartMail(context=order, sender=sender, receiver=receiver, bcc=bcc, subject='Bestellbestätigung Demmelhuber Holz & Raum', text=text, charset=charset)