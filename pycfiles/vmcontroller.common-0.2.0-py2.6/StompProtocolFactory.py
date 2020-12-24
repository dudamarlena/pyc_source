# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/common/StompProtocolFactory.py
# Compiled at: 2011-03-04 15:52:41
"""
StompProtocolFactory
"""
try:
    import logging, pdb, inject, stomper
    from twisted.internet.protocol import ReconnectingClientFactory
    from twisted.internet import reactor
    from vmcontroller.common import support, exceptions
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

class StompProtocolFactory(ReconnectingClientFactory):
    """ Responsible for creating an instance of L{StompProtocol} """
    stompProtocol = inject.attr('stompProtocol')
    initialDelay = delay = 5.0
    factor = 1.0
    jitter = 0.0

    def __init__(self):
        self.protocol = lambda : self.stompProtocol
        self.logger = logging.getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))

    def clientConnectionLost(self, connector, reason):
        self.logger.info('Connection with the broker lost: %s' % reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        self.logger.error('Connection with the broker failed: %s' % reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)