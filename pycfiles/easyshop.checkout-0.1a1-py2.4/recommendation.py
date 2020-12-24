# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/checkout/browser/recommendation.py
# Compiled at: 2008-06-20 09:35:17
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomerManagement

class SendRecommendationView(BrowserView):
    """
    """
    __module__ = __name__

    def getMailInfo(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        shipping_address = am.getShippingAddress()
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        name = shipping_address.getFirstname() + ' '
        name += shipping_address.getLastname()
        return {'email': member.getProperty('email'), 'name': name}