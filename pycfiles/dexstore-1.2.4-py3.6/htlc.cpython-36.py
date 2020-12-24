# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstore/htlc.py
# Compiled at: 2019-03-20 04:11:58
# Size of source mod 2**32: 587 bytes
from .exceptions import HtlcDoesNotExistException
from .blockchainobject import BlockchainObject

class Htlc(BlockchainObject):
    __doc__ = ' Read data about an HTLC contract on the chain\n\n        :param str id: id of the HTLC\n        :param dexstore blockchain_instance: DexStore() instance to use when\n            accesing a RPC\n\n    '
    type_id = 16

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise HtlcDoesNotExistException(self.identifier)
        super(Htlc, self).__init__(data)