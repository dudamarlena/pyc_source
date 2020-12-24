# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/common/StompProtocol.py
# Compiled at: 2011-03-04 15:52:41
"""
StompProtocol
"""
try:
    import logging, pdb, inject, stomper
    from twisted.internet.protocol import Protocol
    from twisted.internet import reactor
    from vmcontroller.common import support, exceptions
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

class StompProtocol(Protocol):
    stompEngine = inject.attr('stompEngine')
    config = inject.attr('config')

    def __init__(self):
        self.logger = logging.getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))
        self._username = self.config.get('broker', 'username')
        self._password = self.config.get('broker', 'password')

    def sendMsg(self, msg):
        self.logger.debug('Sending msg:\n %s' % msg)
        self.transport.write(msg)

    def connectionMade(self):
        """
        Called when a connection is made. 
        Protocol initialization happens here
        """
        self.logger.info('Connection with the broker made')
        stompConnectMsg = stomper.connect(self._username, self._password)
        self.sendMsg(stompConnectMsg)
        try:
            self.factory.resetDelay()
        except:
            pass

    def connectionLost(self, reason):
        """Called when the connection is shut down"""
        self.logger.info('Connection with the broker lost')

    def dataReceived(self, data):
        """Called whenever data is received"""
        reactions = self.stompEngine.react(data)
        if reactions:
            for reaction in filter(None, reactions):
                self.sendMsg(reaction)

        return