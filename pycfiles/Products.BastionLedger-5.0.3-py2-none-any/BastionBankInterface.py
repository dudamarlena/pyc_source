# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/interfaces/BastionBankInterface.py
# Compiled at: 2015-07-18 19:38:10
from zope.interface import Interface

class IBankTool(Interface):
    """
    A Bank tool - control and manage bank account(s), direct debits, direct credits etc
    """


class IBastionBank(Interface):
    """
    All Bank implementaions must support these functions ...
    """

    def _pay(self, amount, account, reference, REQUEST=None):
        """
        returns ZReturnCode
        make a payment
        """
        pass