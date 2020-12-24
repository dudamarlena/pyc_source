# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/File/BetterReading.py
# Compiled at: 2008-10-19 12:19:52
"""=======================
Intelligent File Reader
=======================

This component reads the filename specified at its creation and outputs
it as several messages. When a certain number of messages in its outbox
have not yet been delivered it will pause to reduce memory and CPU usage.
To wake it, ideally Axon should unpause it when the outbox has less than
a certain number of messages (i.e. when some are delivered) but for now
you can send it an arbitrary message (to "inbox") which will wake the
component.
"""
import os, time, fcntl
from Axon.Component import component
from Axon.ThreadedComponent import threadedcomponent
from Axon.Ipc import producerFinished, shutdown
from Kamaelia.IPC import newReader
from Kamaelia.Util.Console import ConsoleReader, ConsoleEchoer
from Kamaelia.Chassis.Pipeline import pipeline
from Kamaelia.Internet.Selector import Selector

class IntelligentFileReader(component):
    """    IntelligentFileReader(filename, chunksize, maxqueue) -> file reading component

    Creates a file reader component. Reads a chunk of chunksize bytes, using the
    Selector to avoid having to block, pausing when the length of its send-queue
    exceeds maxqueue chunks.
    """
    Inboxes = {'inbox': 'wake me up by sending anything here', 
       'control': 'for shutdown signalling', 
       '_selectorready': 'ready to read'}
    Outboxes = {'outbox': 'data output', 
       'debug': 'information designed to aid debugging', 
       'signal': "outputs 'producerFinished' after all data has been read", 
       '_selectorask': 'ask the Selector to notify readiness to read on a file'}

    def __init__(self, filename, chunksize=1024, maxqueue=5):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(IntelligentFileReader, self).__init__()
        self.filename = filename
        self.chunksize = chunksize
        self.maxqueue = maxqueue
        self.chunkbuffer = ''

    def debug(self, msg):
        self.send(msg, 'debug')

    def makeNonBlocking(self, fd):
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)

    def openFile(self, filename):
        return os.open(filename, os.O_RDONLY)

    def selectorWait(self, fd):
        self.debug('selectorWait')
        self.send(newReader(self, ((self, '_selectorready'), fd)), '_selectorask')

    def tryReadChunk(self, fd):
        try:
            data = os.read(fd, self.chunksize)
            if len(data) == 0:
                self.done = True
                return False
            else:
                self.send(data, 'outbox')
                return True
        except OSError, e:
            return False

    def main(self):
        """Main loop"""
        (selectorService, selectorShutdownService, newSelectorService) = Selector.getSelectorServices(self.tracker)
        if newSelectorService:
            newSelectorService.activate()
            self.addChildren(newSelectorService)
        self.link((self, '_selectorask'), selectorService)
        try:
            self.fd = self.openFile(self.filename)
        except Exception, e:
            print e
            return

        self.makeNonBlocking(self.fd)
        self.selectorWait(self.fd)
        self.done = False
        waiting = True
        while not self.done:
            yield 1
            while self.dataReady('inbox'):
                msg = self.recv('inbox')

            if self.dataReady('_selectorready'):
                waiting = False
                msg = self.recv('_selectorready')
            if not waiting:
                readsomething = False
                while len(self.outboxes['outbox']) < self.maxqueue and self.tryReadChunk(self.fd):
                    readsomething = True

                if readsomething:
                    self.selectorWait(self.fd)
                    waiting = True
            if not self.done:
                self.pause()

        self.send(producerFinished(self), 'signal')
        self.debug('IntelligentFileReader terminated')


__kamaelia_components__ = (
 IntelligentFileReader,)
if __name__ == '__main__':

    class DebugOutput(component):

        def main(self):
            while 1:
                yield 1
                self.pause()


    pipeline(ConsoleReader(), IntelligentFileReader('/dev/urandom', 1024, 5), DebugOutput()).run()