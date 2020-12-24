# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/miner.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1095 bytes
from web3.module import Module

class Miner(Module):

    @property
    def hashrate(self):
        return self.web3.manager.request_blocking('eth_hashrate', [])

    def makeDAG(self, number):
        return self.web3.manager.request_blocking('miner_makeDag', [number])

    def setExtra(self, extra):
        return self.web3.manager.request_blocking('miner_setExtra', [extra])

    def setEtherBase(self, etherbase):
        return self.web3.manager.request_blocking('miner_setEtherbase', [etherbase])

    def setGasPrice(self, gas_price):
        return self.web3.manager.request_blocking('miner_setGasPrice', [gas_price])

    def start(self, num_threads):
        return self.web3.manager.request_blocking('miner_start', [num_threads])

    def stop(self):
        return self.web3.manager.request_blocking('miner_stop', [])

    def startAutoDAG(self):
        return self.web3.manager.request_blocking('miner_startAutoDag', [])

    def stopAutoDAG(self):
        return self.web3.manager.request_blocking('miner_stopAutoDag', [])