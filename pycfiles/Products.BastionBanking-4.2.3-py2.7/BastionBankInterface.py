# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/interfaces/BastionBankInterface.py
# Compiled at: 2015-07-18 19:38:10
from zope.interface import Interface

class IBankTool(Interface):
    """
    A Bank tool - control and manage bank account(s), direct debits, direct credits etc
    """
    pass


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