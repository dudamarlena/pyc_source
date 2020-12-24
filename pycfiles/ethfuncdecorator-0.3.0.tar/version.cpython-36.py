# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/version.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 496 bytes
from web3.module import Module

class Version(Module):

    @property
    def api(self):
        from web3 import __version__
        return __version__

    @property
    def node(self):
        return self.web3.manager.request_blocking('web3_clientVersion', [])

    @property
    def network(self):
        return self.web3.manager.request_blocking('net_version', [])

    @property
    def ethereum(self):
        return self.web3.manager.request_blocking('eth_protocolVersion', [])