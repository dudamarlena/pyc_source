# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/customers/browser/manage_payment_methods.py
# Compiled at: 2008-09-03 11:14:43
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import IBankAccount
from easyshop.core.interfaces import IPaymentInformationManagement

class ManagePaymentMethodsView(BrowserView):
    """
    """
    __module__ = __name__

    def deletePaymentMethod(self):
        """
        """
        putils = getToolByName(self.context, 'plone_utils')
        payment_method_id = self.context.request.get('id')
        pm = IPaymentInformationManagement(self.context)
        pm.deletePaymentInformation(payment_method_id)
        if payment_method_id == self.context.selected_payment_information:
            self.context.selected_payment_information = ''
            self.context.selected_payment_method = 'prepayment'
        putils.addPortalMessage('The payment method has been deleted.')
        url = '%s/manage-payment-methods' % self.context.absolute_url()
        self.context.request.response.redirect(url)

    def getDirectDebitAccounts(self):
        """
        """
        pm = IPaymentInformationManagement(self.context)
        return pm.getPaymentInformations(IBankAccount)

    def getCreditCards(self):
        """
        """
        pm = IPaymentInformationManagement(self.context)
        return pm.getPaymentInformations(ICreditCard)