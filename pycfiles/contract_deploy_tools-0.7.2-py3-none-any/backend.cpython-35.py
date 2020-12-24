# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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