# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/devproxy/utils/memcached.py
# Compiled at: 2014-07-28 10:42:31
from twisted.internet import protocol
from twisted.protocols.memcache import MemCacheProtocol

class ReconnectingMemCacheClientFactory(protocol.ReconnectingClientFactory):
    protocol = MemCacheProtocol

    def buildProtocol(self, addr):
        self.client = self.protocol()
        self.addr = addr
        self.client.factory = self
        self.resetDelay()
        return self.client