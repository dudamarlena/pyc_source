# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Codec/Vorbis.py
# Compiled at: 2008-10-19 12:19:52
"""
Simple Vorbis Decoder Component, and Audio Playback Adaptor

"""
import Axon
from Axon.Component import component, scheduler
from Axon.Ipc import producerFinished
import vorbissimple, sys, time, ao

class AOAudioPlaybackAdaptor(component):
    """   AOAudioPlaybackAdaptor() -> new AOAudioPlaybackAdaptor

   Expects to recieve data from standard inbox, and plays it using libao.
   When it recieves a message on the control port:
   Sends a producerConsumed to its outbox.
   Then shutsdown.

   **Requires** libao and pyao (python bindings)

   **Example**

   A simple player::

       Pipeline(
           ReadFileAdaptor("somefile.ogg"),
           VorbisDecode(),
           AOAudioPlaybackAdaptor(),
       ).run()

   """
    Inboxes = {'inbox': 'Any raw PCM encoded data recieved here is played through the default oss playback device', 
       'control': 'If a message is received here, the component shutsdown'}
    Outboxes = {'outbox': 'UNUSED', 
       'signal': 'When the component shutsdown, it sends a producerFinished message out this outbox'}

    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(AOAudioPlaybackAdaptor, self).__init__()
        self.dev = ao.AudioDevice('oss')

    def main(self):
        """Performs the logic described above"""
        playing = True
        while playing:
            if self.dataReady('inbox'):
                buff = self.recv('inbox')
                self.dev.play(buff)
            elif self.dataReady('control'):
                self.recv('control')
                sig = producerFinished(self)
                self.send(sig, 'signal')
                return
            yield 1


class VorbisDecode(component):
    """   VorbisDecode() -> new VorbisDecoder

   A Vorbis decoder accepts data on its inbox "inbox", as would be read
   from an ogg vorbis file, decodes it and sends on the decompressed data on
   out of its outbox "outbox". It doesn't provide any further information
   at this stage, such as bitrate, or any other frills.
   
   **Requires** libvorbissimple and python bindings (see kamaelia downloads)

   **Example**

   A simple player::

       Pipeline(
           ReadFileAdaptor("somefile.ogg"),
           VorbisDecode(),
           AOAudioPlaybackAdaptor(),
       ).run()

   This component expects to recieve OGG VORBIS data as you would
   get from a .ogg file containing vorbis data. (rather than raw
   vorbis data)
   """
    Inboxes = {'inbox': 'Ogg wrapped vorbis data', 'control': 'Receiving a message here causes component shutdown'}
    Outboxes = {'outbox': 'As data is decompresessed it is sent to this outbox', 'signal': 'When the component shuts down, it sends on a producerFinished message'}

    def __init__(self):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(VorbisDecode, self).__init__()
        self.decoder = vorbissimple.vorbissimple()

    def main(self):
        """      This contains no user serviceable parts :-)

      Theory of operation is simple. It simply repeatedly asks the decoder
      object for audio. That decoded audio is sent to the component's outbox.
      If the decoder object responds with RETRY, the component retries.
      If the decoder object responds with NEEDDATA, the component waits
      for data on any inbox until some is available (from an inbox)
      """
        decoding = True
        producerDone = False
        while decoding:
            try:
                data = self.decoder._getAudio()
                self.send(data, 'outbox')
            except 'RETRY':
                pass
            except 'NEEDDATA':
                while not self.dataReady('inbox') > 0 and not self.dataReady('control') > 0:
                    if not producerDone:
                        self.pause()
                        yield 1

                if self.dataReady('inbox'):
                    dataToSend = self.recv('inbox')
                    self.decoder.sendBytesForDecode(dataToSend)
                if self.dataReady('control'):
                    shutdownMessage = self.recv('control')
                    sig = producerFinished(self)
                    self.send(sig, 'signal')
                    producerDone = True
                    decoding = False


__kamaelia_components__ = (
 AOAudioPlaybackAdaptor, VorbisDecode)
if __name__ == '__main__':
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor

    class testHarness(component):

        def __init__(self):
            super(testHarness, self).__init__()
            source = ReadFileAdaptor('./Support/ogg/khangman-splash.ogg', readmode='bitrate', bitrate=400000)
            decoder = VorbisDecode()
            sink = AOAudioPlaybackAdaptor()
            self.source = source
            self.decoder = decoder
            self.sink = sink

        def initialiseComponent(self):
            self.addChildren(self.source, self.decoder, self.sink)
            self.link((self.source, 'outbox'), (self.decoder, 'inbox'))
            self.link((self.source, 'signal'), (self.decoder, 'control'))
            self.link((self.decoder, 'outbox'), (self.sink, 'inbox'))
            self.link((self.decoder, 'signal'), (self.sink, 'control'))
            self.link((self.sink, 'signal'), (self, 'control'))
            self.running = True
            return Axon.Ipc.newComponent(*self.children)

        def mainBody(self):
            if self.dataReady('control'):
                return 0
            return 1


    testHarness().activate()
    scheduler.run.runThreads()