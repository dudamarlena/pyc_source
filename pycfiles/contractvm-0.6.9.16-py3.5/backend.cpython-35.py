# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/backend/backend.py
# Compiled at: 2015-11-18 03:01:10
# Size of source mod 2**32: 971 bytes


class ChainNotSupportedException(Exception):
    pass


class WrongChainException(Exception):
    pass


class Backend:

    def __init__(self):
        raise 'This is an abstract method'

    def connect(self):
        raise 'This is an abstract method'

    def getLastBlockHeight(self):
        raise 'This is an abstract method'

    def getBlockHash(self, index):
        raise 'This is an abstract method'

    def getBlockByHash(self, bhash):
        raise 'This is an abstract method'

    def getTransaction(self, txid):
        raise 'This is an abstract method'

    def broadcastTransaction(self, transaction):
        raise 'This is an abstract method'

    def getBlock(self, index):
        return self.getBlockByHash(self.getBlockHash(index))