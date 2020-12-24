# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/block.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 1168 bytes
from .instance import BlockchainInstance
from graphenecommon.block import Block as GrapheneBlock, BlockHeader as GrapheneBlockHeader

@BlockchainInstance.inject
class Block(GrapheneBlock):
    __doc__ = " Read a single block from the chain\n\n        :param int block: block number\n        :param dexstore.dexstore.DexStore blockchain_instance: DexStore\n            instance\n        :param bool lazy: Use lazy loading\n\n        Instances of this class are dictionaries that come with additional\n        methods (see below) that allow dealing with a block and it's\n        corresponding functions.\n\n        .. code-block:: python\n\n            from dexstore.block import Block\n            block = Block(1)\n            print(block)\n\n        .. note:: This class comes with its own caching function to reduce the\n                  load on the API server. Instances of this class can be\n                  refreshed with ``Account.refresh()``.\n\n    "

    def define_classes(self):
        self.type_id = '-none-'


@BlockchainInstance.inject
class BlockHeader(GrapheneBlockHeader):

    def define_classes(self):
        self.type_id = '-none-'