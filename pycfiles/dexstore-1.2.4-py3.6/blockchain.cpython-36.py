# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/blockchain.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 906 bytes
from .block import Block
from .instance import BlockchainInstance
from dexstorebase import operationids
from graphenecommon.blockchain import Blockchain as GrapheneBlockchain

@BlockchainInstance.inject
class Blockchain(GrapheneBlockchain):
    __doc__ = " This class allows to access the blockchain and read data\n        from it\n\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore\n                 instance\n        :param str mode: (default) Irreversible block (``irreversible``) or\n                 actual head block (``head``)\n        :param int max_block_wait_repetition: (default) 3 maximum wait time for\n            next block ismax_block_wait_repetition * block_interval\n\n        This class let's you deal with blockchain related data and methods.\n    "

    def define_classes(self):
        self.block_class = Block
        self.operationids = operationids