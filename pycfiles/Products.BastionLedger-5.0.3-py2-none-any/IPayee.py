# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/interfaces/IPayee.py
# Compiled at: 2015-07-18 19:38:10
from zope.interface import Interface

class IPayee(Interface):
    """
    API for other objects to interact with BastionBanking to save payee details
    and make payments
    """

    def supportedCurrencies():
        """
        optional list of currencies payable in
        """
        pass

    def defaultCurrency():
        """
        """
        pass

    def getBastionMerchantService():
        """
        """
        pass

    def payeeAmount(self, effective):
        """
        suggested amount to pay
        """
        pass