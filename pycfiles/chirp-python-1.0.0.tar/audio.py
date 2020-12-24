# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\common\audio.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\naudio:    module for playback of audio\n\nCopyright (C) 2011 Daniel Meliza <dan // meliza.org>\nCreated 2011-07-29\n'
try:
    import pyaudio
    _chunksize = 1024

    def play_wave(signal, Fs):
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(signal.dtype.itemsize), channels=1, rate=int(Fs * 1000), output=True)
        stream.write(signal.tostring())
        stream.stop_stream()
        stream.close()
        p.terminate()


except ImportError:

    def play_wave(signal, Fs):
        print 'Unable to import pyaudio; playback not supported'