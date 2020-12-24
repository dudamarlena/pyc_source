# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/backend/chainsoapi.py
# Compiled at: 2015-09-12 08:25:31
# Size of source mod 2**32: 1927 bytes
import requests, json
from .backend import Backend

class ChainSoAPI(Backend):
    SUPPORTED_CHAINS = [
     'BTC', 'XTN', 'DOGE', 'XDT', 'LTC', 'XLT']

    def __init__(self, chain):
        self.chain = chain
        if self.chain == 'BTC':
            self.chainstr = 'BTC'
        else:
            if self.chain == 'XTN':
                self.chainstr = 'BTCTEST'
            else:
                if self.chain == 'DOGE':
                    self.chainstr = 'DOGE'
                else:
                    if self.chain == 'XDT':
                        self.chainstr = 'DOGETEST'
                    else:
                        if self.chain == 'LTC':
                            self.chainstr = 'LTC'
                        elif self.chain == 'XLT':
                            self.chainstr = 'LTCTEST'

    def getSupportedChains():
        return ChainSoAPI.SUPPORTED_CHAINS

    def isChainSupported(chain):
        return chain in ChainSoAPI.SUPPORTED_CHAINS

    def getJsonFromUrl(self, u):
        r = requests.get(u)
        return json.loads(r.text)

    def connect(self):
        pass

    def getLastBlockHeight(self):
        u = 'https://chain.so/api/v2/get_info/' + self.chainstr
        d = self.getJsonFromUrl(u)
        return int(d['data']['blocks'])

    def getBlockHash(self, index):
        u = 'https://chain.so/api/v2/get_blockhash/' + self.chainstr + '/' + str(index)
        d = self.getJsonFromUrl(u)
        return str(d['data']['blockhash'])

    def getBlockByHash(self, bhash):
        u = 'https://chain.so/api/v2/get_block/' + self.chainstr + '/' + str(bhash)
        d = self.getJsonFromUrl(u)
        block = {'height': d['data']['block_no'], 'time': d['data']['time'], 'hash': d['data']['blockhash'], 'tx': d['data']['txs']}
        return block

    def getTransaction(self, txid):
        d = None
        try:
            u = 'https://chain.so/api/v2/get_tx/' + self.chainstr + '/' + str(txid)
            d = self.getJsonFromUrl(u)
            return d['data']['tx_hex']
        except:
            print(u, d)

    def broadcastTransaction(self, transaction):
        raise 'This is an abstract method'