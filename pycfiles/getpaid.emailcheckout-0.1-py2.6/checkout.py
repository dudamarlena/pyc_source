# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/getpaid/emailcheckout/checkout.py
# Compiled at: 2010-05-31 16:45:40
from zope import interface
from Products.PloneGetPaid.preferences import DefaultFormSchemas
from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay

class IUserPaymentInformation(interface.Interface):
    """we don't need credit card information for our processor
    so we define an empty interface.
    """
    pass


class FormSchemas(DefaultFormSchemas):
    interfaces = dict(DefaultFormSchemas.interfaces)
    interfaces['payment'] = IUserPaymentInformation


class CustomCheckoutReviewAndPay(CheckoutReviewAndPay):

    def customise_widgets(self, fields):
        """we don't have any fields we need custom widgets for
        """
        pass