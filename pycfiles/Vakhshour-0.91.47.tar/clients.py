# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: vakhshour/clients.py
# Compiled at: 2012-08-20 04:17:27
from OpenSSL import SSL
from twisted.internet import reactor, ssl
from base import VObject
from protocols import SubscribeFactory

class CtxFactory(ssl.ClientContextFactory):
    """
    Context factory.
    """

    def __init__(self, key, cert):
        self.key = key
        self.cert = cert

    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.use_certificate_file(self.cert)
        ctx.use_privatekey_file(self.key)
        return ctx


class Subscriber(VObject):
    """
    Simplest Subscriber class.
    """

    def __init__(self, host='127.0.0.1', port='7777', secure=False, ssl_key=None, ssl_cert=None):
        self.host = host
        self.secure = secure
        self.port = port
        self.key = ssl_key
        self.cert = ssl_cert
        self.factory = SubscribeFactory()

    def run(self):
        self.logger.info('Connecting to tcp://%s:%s' % (self.host,
         self.port))
        if self.secure:
            self.logger.info('Running on secure mode.')
            reactor.connectSSL(self.host, int(self.port), self.factory, CtxFactory(self.key, self.cert))
        else:
            self.logger.info('Running on non-secure mode.')
            reactor.connectTCP(self.host, int(self.port), self.factory)
        reactor.run()