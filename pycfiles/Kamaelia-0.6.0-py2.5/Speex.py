# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Codec/Speex.py
# Compiled at: 2008-10-19 12:19:52
from sys import path
import Axon, speex, Axon.ThreadedComponent

class SpeexEncode(Axon.ThreadedComponent.threadedcomponent):

    def __init__(self, quality=8):
        super(SpeexEncode, self).__init__()
        self.quality = quality

    def main(self):
        speexobj = speex.new(self.quality, raw=True)
        shutdown = False
        while self.dataReady('inbox') or not shutdown:
            if not self.dataReady('inbox'):
                print '.',
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                ret = speexobj.encode(data)
                if ret is not '':
                    self.send(ret, 'outbox')

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (Axon.Ipc.shutdownMicroprocess, Axon.Ipc.producerFinished)):
                    shutdown = True
                self.send(msg, 'signal')

            if not shutdown:
                self.pause()


class SpeexDecode(Axon.ThreadedComponent.threadedcomponent):

    def __init__(self, quality=8):
        super(SpeexDecode, self).__init__()
        self.quality = quality

    def main(self):
        speexobj = speex.new(self.quality, raw=True)
        shutdown = False
        while self.dataReady('inbox') or not shutdown:
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                ret = speexobj.decode(data)
                if ret:
                    self.send(ret, 'outbox')

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (Axon.Ipc.shutdownMicroprocess, Axon.Ipc.producerFinished)):
                    shutdown = True
                self.send(msg, 'signal')

            if not shutdown:
                self.pause()


__kamaelia_components__ = (SpeexEncode, SpeexDecode)