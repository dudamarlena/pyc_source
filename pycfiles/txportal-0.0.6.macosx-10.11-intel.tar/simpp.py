# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/txportal/simulator/simpp.py
# Compiled at: 2016-03-18 15:06:42
from twisted.internet import utils
from twisted.internet import protocol
import os

class SimProtocol(protocol.ProcessProtocol):

    def __init__(self):
        self.parent_id = os.getpid()

    def connectionMade(self):
        print 'tpsim worker created!'
        print 'master pid = %s' % self.parent_id
        print 'worker pid = %s' % self.transport.pid

    def outReceived(self, data):
        pass

    def errReceived(self, data):
        print 'error', data

    def processExited(self, reason):
        print 'worker exit %s, status %d' % (self.transport.pid, reason.value.exitCode)

    def processEnded(self, reason):
        print '%s worker ended, status %d' % (self.transport.pid, reason.value.exitCode)
        print 'quitting'