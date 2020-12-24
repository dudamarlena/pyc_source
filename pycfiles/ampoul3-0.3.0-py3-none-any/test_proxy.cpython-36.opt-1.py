# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/test/test_proxy.py
# Compiled at: 2017-12-10 09:58:00
# Size of source mod 2**32: 1824 bytes
from twisted.internet import defer, reactor
from twisted.internet.protocol import ClientFactory
from twisted.trial import unittest
from twisted.protocols import amp
from ampoule import service, child, pool
from ampoule.commands import Echo

class ClientAMP(amp.AMP):
    factory = None

    def connectionMade(self):
        if self.factory is not None:
            self.factory.theProto = self
            if hasattr(self.factory, 'onMade'):
                self.factory.onMade.callback(None)


class TestAMPProxy(unittest.TestCase):

    def setUp(self):
        """
        Setup the proxy service and the client connection to the proxy
        service in order to run call through them.

        Inspiration comes from twisted.test.test_amp
        """
        self.pp = pool.ProcessPool()
        self.svc = service.AMPouleService(self.pp, child.AMPChild, 0, '')
        self.svc.startService()
        self.proxy_port = self.svc.server.getHost().port
        self.clientFactory = ClientFactory()
        self.clientFactory.protocol = ClientAMP
        d = self.clientFactory.onMade = defer.Deferred()
        self.clientConn = reactor.connectTCP('127.0.0.1', self.proxy_port, self.clientFactory)
        self.addCleanup(self.clientConn.disconnect)
        self.addCleanup(self.svc.stopService)

        def setClient(_):
            self.client = self.clientFactory.theProto

        return d.addCallback(setClient)

    def test_forwardCall(self):
        """
        Test that a call made from a client is correctly forwarded to
        the process pool and the result is correctly reported.
        """
        DATA = b'hello'
        return self.client.callRemote(Echo, data=DATA).addCallback(self.assertEquals, {'response': DATA})