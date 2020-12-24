# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Audio/PyMedia/Output.py
# Compiled at: 2008-10-19 12:19:52
"""============================
Audio Playback using PyMedia
============================

This component plays raw audio sent to its "inbox" inbox using the pymedia
library.

Example Usage
-------------

Playing 8KHz 16 bit mono raw audio from a file::
    
    Pipeline( RateControlledFileReader("recording.raw", readmode="bytes", rate=8000*2/8,
              Output(sample_rate=8000, channels=1, format="S16_LE"),
            ).run()

How does it work?
-----------------

Output uses the PyMedia library to play back audio to the current audio playback
device.

Send raw binary audio data strings to its "inbox" inbox.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.
"""
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import sys, os
from Axon.ThreadedComponent import threadedcomponent
import time
from math import log
import pymedia.muxer as muxer, pymedia.audio.acodec as acodec, pymedia.audio.sound as sound
from Kamaelia.Support.PyMedia.AudioFormats import format2PyMediaFormat
from Kamaelia.Support.PyMedia.AudioFormats import pyMediaFormat2format
from Kamaelia.Support.PyMedia.AudioFormats import format2BytesPerSample

class Output(threadedcomponent):
    """    Output([sample_rate][,channels][,format]) -> new Output component.
    
    Outputs (plays) raw audio data sent to its "inbox" inbox using the PyMedia
    library.
    
    Keyword arguments:
        
    - sample_rate  -- Sample rate in Hz (default = 44100)
    - channels     -- Number of channels (default = 2)
    - format       -- Sample format (default = "S16_LE")
    """

    def __init__(self, sample_rate=44100, channels=2, format='S16_LE', maximumLag=0.0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Output, self).__init__()
        pformat = format2PyMediaFormat[format]
        self.snd = sound.Output(sample_rate, channels, pformat)
        self.chunksize = sample_rate / 40
        mask = 4 * channels - 1
        self.chunksize = 2 ** int(log(self.chunksize) / log(2))
        self.maxLag = int(maximumLag * sample_rate * channels * format2BytesPerSample[format])

    def main(self):
        CHUNKSIZE = self.chunksize
        shutdown = False
        while self.anyReady() or not shutdown:
            buffer = []
            buffersize = 0
            while self.dataReady('inbox'):
                chunk = self.recv('inbox')
                buffer.append(chunk)
                buffersize += len(chunk)

            if self.maxLag > 0:
                while buffersize > self.maxLag:
                    buffersize -= len(buffer[0])
                    del buffer[0]

            for chunk in buffer:
                for i in range(0, len(chunk), CHUNKSIZE):
                    self.snd.play(chunk[i:i + CHUNKSIZE])

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    shutdown = True
                self.send(msg, 'signal')

            if not shutdown:
                self.pause()

        self.snd.stop()


__kamaelia_components__ = (
 Output,)