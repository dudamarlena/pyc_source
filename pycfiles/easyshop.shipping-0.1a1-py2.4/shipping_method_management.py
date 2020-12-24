# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shipping/adapters/shipping_method_management.py
# Compiled at: 2008-09-03 11:15:18
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IValidity

class ShippingMethodManagement(object):
    """An adapter which provides IShippingMethodManagement for shop content 
    objects.
    """
    __module__ = __name__
    implements(IShippingMethodManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.shipping_methods = self.context.shippingmethods

    def getSelectedShippingMethod(self):
        """
        """
        cm = ICustomerManagement(IShopManagement(self.context).getShop())
        customer = cm.getAuthenticatedCustomer()
        shipping_method_id = customer.selected_shipping_method
        return self.getShippingMethod(shipping_method_id)

    def getShippingMethod(self, id):
        """
        """
        try:
            return self.shipping_methods[id]
        except KeyError:
            return

        return

    def getShippingMethods(self, check_validity=False):
        """
        """
        mtool = getToolByName(self.context, 'portal_membership')
        shipping_methods = []
        for shipping_method in self.shipping_methods.objectValues():
            if check_validity and IValidity(shipping_method).isValid() == False:
                continue
            if mtool.checkPermission('View', shipping_method) is not None:
                shipping_methods.append(shipping_method)

        return shipping_methods