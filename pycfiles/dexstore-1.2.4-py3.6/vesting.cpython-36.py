# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/vesting.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 591 bytes
from .amount import Amount
from .account import Account
from .instance import BlockchainInstance
from graphenecommon.vesting import Vesting as GrapheneVesting

@BlockchainInstance.inject
class Vesting(GrapheneVesting):
    __doc__ = ' Read data about a Vesting Balance in the chain\n\n        :param str id: Id of the vesting balance\n        :param dexstore blockchain_instance: DexStore() instance to use when\n            accesing a RPC\n\n    '

    def define_classes(self):
        self.type_id = 13
        self.account_class = Account
        self.amount_class = Amount