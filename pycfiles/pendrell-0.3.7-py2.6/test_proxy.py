# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/cases/test_proxy.py
# Compiled at: 2010-09-03 02:22:19
import random
from twisted.internet.defer import inlineCallbacks
from twisted.internet import error as netErr, protocol, reactor
from twisted.protocols import socks
from twisted.python import failure, log
from twisted.trial import unittest
from pendrell import agent as pendrell, error, protocols, proxy
from pendrell.cases.test_jigsaw import JigsawTestMixin as _JiggyTest
from pendrell.cases.util import PendrellTestMixin, trialIsOnline

class SOCKSv4TestMixin(object):
    _lo0 = '127.0.0.1'
    socks_port = random.choice(range(1000, 65536))

    def setUp(self):
        f = socks.SOCKSv4Factory('socks.log')
        self.socksServer = reactor.listenTCP(self.socks_port, f, interface=self._lo0)
        socksClient = proxy.SOCKSv4Proxy('socks', self._lo0, self.socks_port)
        self.agent = pendrell.Agent(proxyer=proxy.Proxyer(socksClient), timeout=self.timeout / 2)

    @inlineCallbacks
    def tearDown(self):
        yield self.agent.cleanup()
        yield self.socksServer.stopListening()


class SOCKSv4JigsawTest(SOCKSv4TestMixin, _JiggyTest, unittest.TestCase):
    timeout = 20
    if not trialIsOnline:
        skip = 'Offline mode'