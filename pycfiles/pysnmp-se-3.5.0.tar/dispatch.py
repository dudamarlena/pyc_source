# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/carrier/twisted/dispatch.py
# Compiled at: 2019-08-18 17:24:05
import sys, time, traceback
from twisted.internet import reactor, task
from pysnmp.carrier.base import AbstractTransportDispatcher
from pysnmp.error import PySnmpError

class TwistedDispatcher(AbstractTransportDispatcher):
    """TransportDispatcher based on twisted.internet.reactor"""
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        AbstractTransportDispatcher.__init__(self)
        self.__transportCount = 0
        if 'timeout' in kwargs:
            self.setTimerResolution(kwargs['timeout'])
        self.loopingcall = task.LoopingCall(lambda self=self: self.handleTimerTick(time.time()))

    def runDispatcher(self, timeout=0.0):
        if not reactor.running:
            try:
                reactor.run()
            except KeyboardInterrupt:
                raise
            except:
                raise PySnmpError('reactor error: %s' % (';').join(traceback.format_exception(*sys.exc_info())))

    def registerTransport(self, tDomain, transport):
        if not self.loopingcall.running and self.getTimerResolution() > 0:
            self.loopingcall.start(self.getTimerResolution(), now=False)
        AbstractTransportDispatcher.registerTransport(self, tDomain, transport)
        self.__transportCount += 1

    def unregisterTransport(self, tDomain):
        t = AbstractTransportDispatcher.getTransport(self, tDomain)
        if t is not None:
            AbstractTransportDispatcher.unregisterTransport(self, tDomain)
            self.__transportCount -= 1
        if self.__transportCount == 0 and self.loopingcall.running:
            self.loopingcall.stop()
        return