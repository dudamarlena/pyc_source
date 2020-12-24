# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/pyvnc2swf/record_sound.py
# Compiled at: 2011-03-28 15:09:52
import sys, time, pymedia.audio.sound as sound, pymedia.audio.acodec as acodec, pymedia.muxer as muxer, threading

class voiceRecorder:

    def __init__(self, name):
        self.name = name
        self.finished = False

    def record(self):
        self.snd.start()
        while not self.finished:
            s = self.snd.getData()
            if s and len(s):
                for fr in self.ac.encode(s):
                    block = self.mux.write(self.stream_index, fr)
                    if block is not None:
                        self.f.write(block)

            else:
                time.sleep(0.003)

        self.snd.stop()
        return

    def run(self):
        print 'recording to', self.name
        self.f = open(self.name, 'wb')
        cparams = {'id': acodec.getCodecID('mp3'), 'bitrate': 128000, 
           'sample_rate': 44100, 
           'channels': 1}
        self.ac = acodec.Encoder(cparams)
        self.snd = sound.Input(44100, 1, sound.AFMT_S16_LE)
        self.mux = muxer.Muxer('mp3')
        self.stream_index = self.mux.addStream(muxer.CODEC_TYPE_AUDIO, self.ac.getParams())
        block = self.mux.start()
        if block:
            self.f.write(block)
        self.finished = False
        thread = threading.Thread(target=self.record)
        thread.start()
        try:
            while not self.finished:
                time.sleep(0.003)

        except KeyboardInterrupt:
            self.finished = True

        print 'finishing recording to', self.name
        thread.join()
        footer = self.mux.end()
        if footer is not None:
            self.f.write(footer)
        self.f.close()
        print 'finished recording to', self.name
        print 'snipping leading zeroes...'
        f = open(self.name, 'rb')
        buffer = f.read()
        f.close()
        buffer = buffer.lstrip(chr(0))
        f = open(self.name, 'wb')
        f.write(buffer)
        f.close()
        print 'snipped leading zeroes'
        return


if __name__ == '__main__':
    import time
    if len(sys.argv) != 2:
        print 'Usage: %s <file_name>' % sys.argv[0]
    else:
        voiceRecorder(sys.argv[1]).run()