# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/child.py
# Compiled at: 2017-12-10 09:58:00
# Size of source mod 2**32: 1743 bytes
from twisted.python import log
from twisted.internet import error
from twisted.protocols import amp
from ampoule.commands import Echo, Shutdown, Ping

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
        log.msg('Shutdown message received, goodbye.')
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