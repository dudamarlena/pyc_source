# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/witness.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 1089 bytes
from .account import Account
from .blockchainobject import BlockchainObject
from .instance import BlockchainInstance
from graphenecommon.witness import Witness as GrapheneWitness, Witnesses as GrapheneWitnesses

@BlockchainInstance.inject
class Witness(GrapheneWitness):
    __doc__ = ' Read data about a witness in the chain\n\n        :param str account_name: Name of the witness\n        :param dexstore blockchain_instance: DexStore() instance to use when\n               accesing a RPC\n\n    '

    def define_classes(self):
        self.account_class = Account
        self.type_ids = [6, 2]


@BlockchainInstance.inject
class Witnesses(GrapheneWitnesses):
    __doc__ = ' Obtain a list of **active** witnesses and the current schedule\n\n        :param bool only_active: (False) Only return witnesses that are\n            actively producing blocks\n        :param dexstore blockchain_instance: DexStore() instance to use when\n            accesing a RPC\n    '

    def define_classes(self):
        self.account_class = Account
        self.witness_class = Witness