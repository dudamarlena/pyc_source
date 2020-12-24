# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/recharge/__init__.py
# Compiled at: 2019-10-30 11:12:26
# Size of source mod 2**32: 734 bytes
from .resources import RechargeAddress, RechargeCharge, RechargeCheckout, RechargeCustomer, RechargeOrder, RechargeSubscription

class RechargeAPI(object):

    def __init__(self, access_token=None, log_debug=False):
        self.access_token = access_token
        self.log_debug = log_debug
        kwargs = {'access_token':access_token, 
         'log_debug':log_debug}
        self.Address = RechargeAddress(**kwargs)
        self.Charge = RechargeCharge(**kwargs)
        self.Checkout = RechargeCheckout(**kwargs)
        self.Customer = RechargeCustomer(**kwargs)
        self.Order = RechargeOrder(**kwargs)
        self.Subscription = RechargeSubscription(**kwargs)