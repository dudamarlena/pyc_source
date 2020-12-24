# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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