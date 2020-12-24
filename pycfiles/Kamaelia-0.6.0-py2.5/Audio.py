# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/Audio.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.Audio.PyMedia.Input import Input as _SoundInput
from Kamaelia.Audio.PyMedia.Output import Output as _SoundOutput
from Kamaelia.Audio.RawAudioMixer import RawAudioMixer as _RawAudioMixer

def SoundInput():
    return _SoundInput(channels=1, sample_rate=8000, format='S16_LE')


def SoundOutput():
    return _SoundOutput(channels=1, sample_rate=8000, format='S16_LE', maximumLag=0.25)


def RawAudioMixer():
    return _RawAudioMixer(sample_rate=8000, channels=1, format='S16_LE', readThreshold=0.2, bufferingLimit=0.4, readInterval=0.05)