# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/dapp.py
# Compiled at: 2015-11-05 12:17:12
# Size of source mod 2**32: 1766 bytes
from .proto import Protocol

class Dapp:

    def __init__(self, dapp_code, methods, chain, database, dht, api=None):
        self.DappCode = dapp_code
        self.Methods = methods
        self.Database = database
        self.Chain = chain
        self.DHT = dht
        self.API = api

    def getAPI(self):
        return self.API

    def handleMessage(self, message):
        pass


class API:

    def __init__(self, core, dht, rpcmethods, errors):
        self.core = core
        self.dht = dht
        self.errors = errors
        self.rpcmethods = rpcmethods

    def getRPCMethods(self):
        return self.rpcmethods

    def createTransactionResponse(self, message):
        datahash, outscript, tempid = message.toOutputScript(self.dht)
        return {'outscript': outscript, 'datahash': datahash, 'tempid': tempid, 'fee': Protocol.estimateFee(self.core.getChainCode())}

    def createErrorResponse(self, error):
        if error in self.errors:
            return {'error': self.errors[error]['code'], 'message': self.errors[error]['message']}
        else:
            return {'error': -1, 'message': 'General error (' + str(error) + ')'}


class Core:

    def __init__(self, chain, database):
        self.chain = chain
        self.database = database

    def getTime(self, height=None):
        if height != None:
            return int(int(height) / Protocol.TIME_UNIT_BLOCKS)
        return int(int(self.chain.getChainHeight()) / Protocol.TIME_UNIT_BLOCKS)

    def getChainName(self):
        return self.chain.getChainName()

    def getChainCode(self):
        return self.chain.getChainCode()

    def getChainHeight(self):
        return int(self.chain.getChainHeight())