# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/olauzanne/workspace/paguro/getpaid.clickandbuy/getpaid/clickandbuy/clickandbuy.py
# Compiled at: 2009-01-30 04:18:04
from Products.CMFCore.utils import getToolByName
from zope import interface
from interfaces import IClickAndBuyStandardOptions, IClickAndBuyStandardProcessor
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core import interfaces as GetPaidInterfaces

class ClickAndBuyStandardProcessor(object):
    __module__ = __name__
    options_interface = IClickAndBuyStandardOptions
    interface.implements(IClickAndBuyStandardProcessor)

    def __init__(self, context):
        self.context = context

    def cart_post_button(self, order):
        price = int(order.getTotalPrice() * 100)
        price = 100
        order_id = order.order_id
        options = IClickAndBuyStandardOptions(self.context)
        siteroot = getToolByName(self.context, 'portal_url').getPortalObject()
        manage_options = IGetPaidManagementOptions(siteroot)
        premium_url = options.premium_url
        transaction_url = 'https://eu.clickandbuy.com/newauth/%s/@@transaction?price=%s&externalBDRID=%s'
        transaction_url = transaction_url % (premium_url, price, order_id)
        img_url = 'https://eu.clickandbuy.com/images/all/logos/powredby_logo_en.gif'
        alt = 'Pay with Click and Buy'
        return "<a href='%s'><img src='%s' alt='%s'></a>" % (transaction_url, img_url, alt)

    def capture(self, order, price):
        return GetPaidInterfaces.keys.results_async

    def authorize(self, order, payment):
        pass