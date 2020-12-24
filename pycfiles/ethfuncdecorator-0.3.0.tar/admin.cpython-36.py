# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/admin.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1277 bytes
from web3.module import Module

class Admin(Module):

    def addPeer(self, node_url):
        return self.web3.manager.request_blocking('admin_addPeer', [node_url])

    @property
    def datadir(self):
        return self.web3.manager.request_blocking('admin_datadir', [])

    @property
    def nodeInfo(self):
        return self.web3.manager.request_blocking('admin_nodeInfo', [])

    @property
    def peers(self):
        return self.web3.manager.request_blocking('admin_peers', [])

    def setSolc(self, solc_path):
        return self.web3.manager.request_blocking('admin_setSolc', [solc_path])

    def startRPC(self, host='localhost', port='8545', cors='', apis='eth,net,web3'):
        return self.web3.manager.request_blocking('admin_startRPC', [
         host, port, cors, apis])

    def startWS(self, host='localhost', port='8546', cors='', apis='eth,net,web3'):
        return self.web3.manager.request_blocking('admin_startWS', [
         host, port, cors, apis])

    def stopRPC(self):
        return self.web3.manager.request_blocking('admin_stopRPC', [])

    def stopWS(self):
        return self.web3.manager.request_blocking('admin_stopWS', [])