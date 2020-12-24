# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/interfaces/BastionMerchantInterface.py
# Compiled at: 2015-07-18 19:38:10
from zope.interface import Interface

class IMerchantTool(Interface):
    """
    A Merchant tool - control and manage merchant payments
    """

    def supportedCurrencies():
        """
        """
        pass

    def manage_payTransaction(txn, reference='', payee=None):
        """
        """
        pass

    def manage_refund(payment):
        """
        """
        pass

    def manage_reconcile(payment):
        """
        """
        pass

    def manage_accept(payment):
        """
        if this payment has been accepted, then post the transaction associated with it
        """
        pass

    def manage_reject(payment):
        """
        if this payment is not successful, then cancel the transaction associated with it
        """
        pass


class IBastionMerchant(Interface):
    """
    All Bank implementaions must support these functions ...
    """

    def __init__(id):
        """
        a default constructor is necessary ...
        """
        pass

    def supportedCurrencies():
        """
        return a tuple of the currency codes supported by the underlying transport
        """
        pass

    def serviceLogo():
        """
        the logo of the service to display on forms
        """
        pass

    def serviceUrl():
        """
        the url of the service, for legitimacy/info on forms
        """
        pass

    def _generateBastionPayment(id, amount, ref='', REQUEST={}):
        """
        take whatever was in the form and return a BastionPayment, with whatever's
        appropriate as payee

        not all merchant transactions are against credit cards, this allows us to
        pass an agreed format between function calls
        """
        pass

    def _pay(payee, amount, REQUEST=None):
        """
        returns returncode, redirect_url
        
        take client's credit card details and transact against it

        all parameters are passed in the request, allowing variable parameters ...

        this is a private function and should be called by BastionMerchantService (or
        some other function that has verified the input parameters)

        the redirect_url should be '' for gateways that don't hijack your customer
        """
        pass

    def _refund(payee, amount, ref, REQUEST=None):
        """
        returns returncode
        
        take client's credit card details and transact against it

        all parameters are passed in the request, allowing variable parameters ...

        this is a private function and should be called by BastionMerchantService (or
        some other function that has verified the input parameters)
        """
        pass

    def widget():
        """
        returns the form elements needed to make a payment for ZMI
        """
        pass

    def getTransaction(pmt):
        """
        returns a dict of details about the payment held by the provider
        """
        pass

    def merchantAccount(Ledger):
        """
        get the bank account associated with the merchant from the ledger (should
        be identified by a tag of the merchant service name
        """
        pass

    def merchantFee(amount):
        """
        return the merchant charge for processing the amount
        """
        pass