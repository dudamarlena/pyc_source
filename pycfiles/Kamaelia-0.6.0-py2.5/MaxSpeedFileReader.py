# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/File/MaxSpeedFileReader.py
# Compiled at: 2008-10-19 12:19:52
"""==================================
Reading a file as fast as possible
==================================

MaxSpeedFileReader reads a file in bytes mode as fast as it can; limited only
by any size limit on the inbox it is sending the data to.

This component is therefore useful for building systems that are self rate
limiting - systems that are just trying to process data as fast as they can and
are limited by the speed of the slowest part of the chain.

Example Usage
-------------

Read "myfile" in in chunks of 1024 bytes. The rate is limited by the rate at
which the consumer component can consume the chunks, since its inbox has a size
limit of 5 items of data::

    consumer = Consumer()
    consumer.inboxes["inbox"].setSize(5)
    
    Pipeline( MaxSpeedFileReader("myfile", chunksize=1024),
              consumer,
            ).run()

More details
------------

Specify a filename and chunksize and MaxSpeedFileReader will read bytes from
the file in the chunksize you specified and send them out of its "outbox"
outbox.

If the destination inbox it is sending chunks to is size limited, then
MaxSpeedFileReader will pause until space becomes available. This is how the
speed at which the file is ingested is regulated - by the rate at which it is
consumed.

When the whole file has been read, this component will terminate and send a
producerFinished() message out of its "signal" outbox.

If a producerFinished message is received on the "control" inbox, this component
will complete sending any data that may be waiting. It will then send the
producerFinished message on out of its "signal" outbox and terminate.

If a shutdownMicroprocess message is received on the "control" inbox, this
component will immediately send it on out of its "signal" outbox and immediately
terminate. It will not complete sending on any pending data.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox

class MaxSpeedFileReader(component):
    """    MaxSpeedFileReader(filename[,chunksize]) -> new MaxSpeedFileReader component.

    Reads the contents of a file in bytes mode; sending it out as fast as it can
    in chunks from the "outbox" outbox. The rate of reading is only limited by
    any size limit of the destination inbox to which the data is being sent.
    
    Keyword arguments:

    - filename   -- The filename of the file to read
    - chunksize  -- Optional. The maximum number of bytes in each chunk of data read from the file and sent out of the "outbox" outbox (default=32768)
    """

    def __init__(self, filename, chunksize=32768):
        super(MaxSpeedFileReader, self).__init__()
        self.filename = filename
        self.chunksize = chunksize

    def handleControl(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished, shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)

    def waitSend(self, data, boxname):
        while 1:
            try:
                self.send(data, boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise 'STOP'
                self.pause()
                yield 1
                if self.mustStop():
                    raise 'STOP'

    def main(self):
        self.shutdownMsg = ''
        fh = open(self.filename, 'rb')
        try:
            while 1:
                data = fh.read(self.chunksize)
                if data == '':
                    self.shutdownMsg = producerFinished(self)
                    raise 'STOP'
                for _ in self.waitSend(data, 'outbox'):
                    yield _

                if self.mustStop():
                    raise 'STOP'

        except 'STOP':
            self.send(self.shutdownMsg, 'signal')


__kamaelia_components__ = (
 MaxSpeedFileReader,)