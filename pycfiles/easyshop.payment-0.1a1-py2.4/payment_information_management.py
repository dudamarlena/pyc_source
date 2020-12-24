# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/adapters/payment_information_management.py
# Compiled at: 2008-09-03 11:15:12
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.exceptions import BadRequest
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentInformation
from easyshop.core.interfaces import IValidity

class PaymentInformationManagement:
    """
    """
    __module__ = __name__
    implements(IPaymentInformationManagement)
    adapts(ICustomer)

    def __init__(self, context):
        """
        """
        self.context = context

    def deletePaymentInformation(self, id):
        """
        """
        try:
            self.context.manage_delObjects(id)
        except BadRequest:
            return False
        else:
            return True

    def getPaymentInformation(self, id):
        """
        """
        try:
            return self.context[id]
        except KeyError:
            return

        return

    def getPaymentInformations(self, interface=IPaymentInformation, check_validity=False):
        """Returns the payment information of a customer.
        """
        mtool = getToolByName(self.context, 'portal_membership')
        result = []
        for object in self.context.objectValues():
            if interface.providedBy(object) == False:
                continue
            if check_validity == True and IValidity(object).isValid(object) == False:
                continue
            if mtool.checkPermission('View', object) is not None:
                result.append(object)

        return result

    def getSelectedPaymentInformation(self, check_validity=False):
        """
        """
        try:
            selected_payment_information = self.context[self.context.selected_payment_information]
        except KeyError:
            return

        if check_validity == False or IValidity(selected_payment_information).isValid() == True:
            return selected_payment_information
        else:
            return
        return

    def getSelectedPaymentMethod(self, check_validity=False):
        """
        """
        try:
            selected_payment_method = self.context.paymentmethods[self.context.selected_payment_method]
        except KeyError:
            return self.context.paymentmethods['prepayment']

        if check_validity == False or IValidity(selected_payment_method).isValid() == True:
            return selected_payment_method
        else:
            return self.context.paymentmethods['prepayment']