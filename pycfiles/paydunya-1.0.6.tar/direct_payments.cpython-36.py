# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/freedev/Code/OpenSource/paydunya-python/paydunya/direct_payments.py
# Compiled at: 2017-08-18 23:09:15
# Size of source mod 2**32: 641 bytes
"""PAYDUNYA DirectPay"""
from . import Payment

class DirectPay(Payment):
    __doc__ = 'Directpay processing class\n\n    Receipient account_info format:\n    \'{\n       "account_alias" : "774563209",\n       "amount" : 215000\n    }\'\n    '

    def __init__(self, account_alias=None, amount=None):
        self.transaction = {'account_alias':account_alias, 
         'amount':amount}
        super(DirectPay, self).__init__()

    def process(self, transaction=None):
        """Process the transaction"""
        return self._process('direct-pay/credit-account', transaction or self.transaction)