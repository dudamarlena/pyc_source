# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/committee.py
# Compiled at: 2019-03-20 04:08:36
# Size of source mod 2**32: 589 bytes
from .account import Account
from .instance import BlockchainInstance
from graphenecommon.committee import Committee as GrapheneCommittee

@BlockchainInstance.inject
class Committee(GrapheneCommittee):
    __doc__ = ' Read data about a Committee Member in the chain\n\n        :param str member: Name of the Committee Member\n        :param dexstore blockchain_instance: DexStore() instance to use when\n            accesing a RPC\n        :param bool lazy: Use lazy loading\n\n    '

    def define_classes(self):
        self.type_id = 5
        self.account_class = Account