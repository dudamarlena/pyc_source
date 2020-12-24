# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Audio/Codec/PyMedia/Decoder.py
# Compiled at: 2008-10-19 12:19:52
"""=======================================
Compressed audio decoding using PyMedia
=======================================

Decodes compressed audio data sent to its "inbox" inbox and outputs the raw
audio data from its "outbox" outbox. Decoding done using the PyMedia library.

Example Usage
-------------

Playing a MP3 file, known to be 128bkps, 44100Hz 16bit stereo::
    
    Pipeline( RateControlledFileReader("my.mp3", readmode="bytes", rate=128*1024/8),
              Decoder("mp3"),
              Output(44100, 2, "S16_LE"),
            ).run()

How does it work?
-----------------

Set up Decoder by specifying the filetype/codec to the initializer. What codecs
are supported depends on your PyMedia installation.

Send raw binary data strings containing the compressed audio data to the "inbox"
inbox, and raw binary data strings containing the uncompressed raw audio data
will be sent out of the "outbox" outbox.

This component will terminate if a shutdownMicroprocess or producerFinished
message is sent to the "control" inbox. The message will be forwarded on out of
the "signal" outbox just before termination.

"""
from Axon.Component import component
from Axon.Ipc import shutdownMicroprocess, producerFinished
import pymedia.muxer as muxer, pymedia.audio.acodec as acodec, pymedia.audio.sound as sound, sys, os
from Kamaelia.Support.PyMedia.AudioFormats import codec2fileExt
from Kamaelia.Support.PyMedia.AudioFormats import pyMediaFormat2format

class Decoder(component):
    """    Decoder(fileExtension) -> new pymedia Audio Decoder.
    
    Send raw data from a compressed audio file (which had the specified extension)
    to the "inbox" inbox, and decompressed blocks of raw audio data are emitted
    from the "outbox" outbox.
    
    Keyword  arguments:

    - codec  -- The codec (ones supported depend on your local installation)
    """
    Inboxes = {'inbox': 'compressed audio data', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'raw audio samples', 'format': 'dictionary detailing sample_rate, sample_format and channels', 
       'needData': 'requests for more data (value is suggested minimum number of bytes', 
       'signal': 'Shutdown signalling'}

    def __init__(self, codec):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Decoder, self).__init__()
        self.extension = codec2fileExt[codec]

    def main(self):
        dm = muxer.Demuxer(self.extension)
        shutdown = False
        decoder = None
        while self.anyReady() or not shutdown:
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                frames = dm.parse(data)
                for frame in frames:
                    if not decoder:
                        stream_index = frame[0]
                        decoder = acodec.Decoder(dm.streams[stream_index])
                        decoded = decoder.decode(frame[1])
                        format = {'channels': decoded.channels, 
                           'sample_rate': decoded.sample_rate, 
                           'format': pyMediaFormat2format[sound.AFMT_S16_LE]}
                        self.send(format, 'format')
                    else:
                        decoded = decoder.decode(frame[1])
                    self.send(str(decoded.data), 'outbox')

            self.send(4096, 'needData')
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                    shutdown = True
                self.send(msg, 'signal')

            if not shutdown:
                self.pause()
            yield 1

        return


__kamaelia_components__ = (
 Decoder,)