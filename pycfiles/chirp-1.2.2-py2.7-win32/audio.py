# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\common\audio.py
# Compiled at: 2013-12-11 23:17:46
"""
audio:    module for playback of audio

Copyright (C) 2011 Daniel Meliza <dan // meliza.org>
Created 2011-07-29
"""
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