# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Audio/PyMedia/Input.py
# Compiled at: 2008-10-19 12:19:52
"""===========================
Audio Capture using PyMedia
===========================

This component captures raw audio using the pymedia library, and outputs it
out of its "outbox" outbox.

Example Usage
-------------

Recording telephone quality audio to a file::
    
    Pipeline( Input(sample_rate=8000, channels=1, format="S16_LE"),
              SimpleFileWriter("recording.raw"),
            ).run()

How does it work?
-----------------

Input uses the PyMedia library to capture audio from the currently selected
audio capture device.

It outputs to its "outbox" outbox raw binary audio data in strings.

This component supports sending to a size limited inbox. If the size limited
inbox is full, this component will pause until it is able to send out the data.

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
import pymedia.audio.acodec as acodec, pymedia.audio.sound as sound
from Kamaelia.Support.PyMedia.AudioFormats import format2PyMediaFormat

class Input(threadedcomponent):
    """    Input([sample_rate][,channels][,format]) -> new Input component.
    
    Captures audio using the PyMedia library and sends the raw audio data out
    of its "outbox" outbox.
    
    Keyword arguments:
        
    - sample_rate  -- Sample rate in Hz (default = 44100)
    - channels     -- Number of channels (default = 2)
    - format       -- Sample format (default = "S16_LE")
    """
    Outboxes = {'outbox': 'raw audio samples', 'format': 'dictionary detailing sample_rate, sample_format and channels', 
       'signal': 'Shutdown signalling'}

    def __init__(self, sample_rate=44100, channels=2, format='S16_LE'):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Input, self).__init__()
        pformat = format2PyMediaFormat[format]
        self.snd = sound.Input(sample_rate, channels, pformat)
        self.sample_rate = sample_rate
        self.channels = channels
        self.format = format

    def main(self):
        self.snd.start()
        format = {'channels': self.channels, 
           'sample_rate': self.sample_rate, 
           'format': self.format}
        self.send(format, 'format')
        shutdown = False
        while self.anyReady() or not shutdown:
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    shutdown = True
                self.send(msg, 'signal')

            raw = self.snd.getData()
            if raw and len(raw):
                data = str(raw)
                while data:
                    try:
                        self.send(data, 'outbox')
                        data = None
                    except noSpaceInBox:
                        self.pause()

            else:
                self.pause(0.01)

        self.snd.stop()
        return


__kamaelia_components__ = (
 Input,)