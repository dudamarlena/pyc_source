# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/adapters/payment_method_management.py
# Compiled at: 2008-09-03 11:15:12
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import IPaymentMethod
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import ISelectablePaymentMethod
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IValidity

class PaymentMethodManagement(object):
    """An adapter which provides IPaymentMethodManagement for shop content
    objects.
    """
    __module__ = __name__
    implements(IPaymentMethodManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.paymentmethods = self.context.paymentmethods

    def deletePaymentMethod(self, id):
        """
        """
        try:
            self.context.paymentmethods.manage_delObjects(id)
        except AttributeError:
            return False

        return True

    def getPaymentMethod(self, id):
        """Returns payment method by given id.
        """
        try:
            return self.paymentmethods[id]
        except KeyError:
            return

        return

    def getPaymentMethods(self, check_validity=False):
        """Returns the payment methods on shop level. 
        """
        mtool = getToolByName(self.context, 'portal_membership')
        result = []
        for object in self.paymentmethods.objectValues():
            if IPaymentMethod.providedBy(object) == False:
                continue
            if check_validity and IValidity(object).isValid(object) == False:
                continue
            if mtool.checkPermission('View', object) is not None:
                result.append(object)

        return result

    def getSelectablePaymentMethods(self, check_validity=False):
        """Returns payment method which are selectable by a customer.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        result = []
        for object in self.paymentmethods.objectValues():
            if ISelectablePaymentMethod.providedBy(object) == False:
                continue
            if check_validity and IValidity(object).isValid(object) == False:
                continue
            if mtool.checkPermission('View', object) is not None:
                result.append(object)

        return result