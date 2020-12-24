# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Util/Chunkifier.py
# Compiled at: 2008-10-19 12:19:52
"""==========
Chunkifier
==========

A component that fixes the message size of an input stream to a given value,
outputting blocks of that size when sufficient input has accumulated. This
component's input is stream orientated - all messages received are
concatenated to the interal buffer without divisions.

Example Usage
-------------

Chunkifying a console reader::

    pipeline(
        ConsoleReader(eol=""),
        Chunkifier(20),
        ConsoleEchoer()
    ).run()

How does it work?
-----------------

Messages received on the "inbox" are buffered until at least N bytes have
been collected. A message containing those first N bytes is sent out
"outbox". A CharacterFIFO object is used to do this in linear time.

The usual sending of a producerFinished/shutdown to the "control"
inbox will shut it down.
"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdown
import string

class CharacterFIFO(object):
    """An efficient character queue type (designed to work in O(n) time for n characters)."""

    def __init__(self):
        self.queuearray = []
        self.length = 0
        self.startboundary = 0

    def push(self, text):
        self.queuearray.append(text)
        self.length += len(text)

    def __len__(self):
        return self.length

    def poplength(self, length):
        if len(self) < length:
            raise IndexError
        else:
            thischunk = []
            sizeneeded = length
            while 1:
                chunk = self.queuearray[0]
                sizeneeded -= len(chunk) - self.startboundary
                if sizeneeded < 0:
                    thischunk.append(chunk[self.startboundary:len(chunk) + sizeneeded])
                    self.startboundary = len(chunk) + sizeneeded
                else:
                    if self.startboundary > 0:
                        thischunk.append(chunk[self.startboundary:])
                    else:
                        thischunk.append(chunk)
                    self.queuearray.pop(0)
                    self.startboundary = 0
                if sizeneeded <= 0:
                    break

            self.length -= length
            return string.join(thischunk, '')


class Chunkifier(component):
    """    Chunkifier([chunksize]) -> new Chunkifier component.
    
    Flow controller - collects incoming data and outputs it only as quanta of
    a given length in bytes (chunksize), unless the input stream ends (producerFinished). 
    
    Keyword arguments:
    - chunksize  -- Chunk size in bytes
    - nodelay    -- if set to True, partial chunks will be output rather than buffering up data while waiting for more to arrive.
    """
    Inboxes = {'inbox': 'Data stream to be split into chunks', 
       'control': 'Shut me down'}
    Outboxes = {'outbox': 'Each message is a chunk', 
       'signal': "I've shut down"}

    def __init__(self, chunksize=1048576, nodelay=False):
        super(Chunkifier, self).__init__()
        self.forwardqueue = CharacterFIFO()
        self.chunksize = chunksize
        self.nodelay = nodelay

    def sendPartialChunk(self):
        if len(self.forwardqueue) > 0:
            self.send(self.forwardqueue.poplength(len(self.forwardqueue)), 'outbox')

    def sendChunk(self):
        self.send(self.forwardqueue.poplength(self.chunksize), 'outbox')

    def main(self):
        while 1:
            yield 1
            while self.dataReady('inbox'):
                msg = self.recv('inbox')
                self.forwardqueue.push(msg)

            while len(self.forwardqueue) >= self.chunksize:
                self.sendChunk()

            if self.nodelay:
                self.sendPartialChunk()
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished):
                    self.sendPartialChunk()
                    self.send(producerFinished(self), 'signal')
                    return
                elif isinstance(msg, shutdown):
                    self.send(producerFinished(self), 'signal')
                    return

            self.pause()


__kamaelia_components__ = (Chunkifier,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import pipeline
    from Kamaelia.Util.Console import ConsoleEchoer, ConsoleReader
    pipeline(ConsoleReader(eol=''), Chunkifier(10), ConsoleEchoer()).run()