# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ampoule/child.py
# Compiled at: 2019-09-15 01:25:44
# Size of source mod 2**32: 1767 bytes
from twisted import logger
from twisted.internet import error
from twisted.protocols import amp
from ampoule.commands import Echo, Shutdown, Ping
log = logger.Logger()

class AMPChild(amp.AMP):

    def __init__(self):
        super(AMPChild, self).__init__(self)
        self.shutdown = False

    def connectionLost(self, reason):
        amp.AMP.connectionLost(self, reason)
        from twisted.internet import reactor
        try:
            reactor.stop()
        except error.ReactorNotRunning:
            pass

        if not self.shutdown:
            import os
            os._exit(-1)

    def shutdown(self):
        """
        This method is needed to shutdown the child gently without
        generating an exception.
        """
        log.info('Shutdown message received, goodbye.')
        self.shutdown = True
        return {}

    Shutdown.responder(shutdown)

    def ping(self):
        """
        Ping the child and return an answer
        """
        return {'response': 'pong'}

    Ping.responder(ping)

    def echo(self, data):
        """
        Echo some data through the child.
        """
        return {'response': data}

    Echo.responder(echo)