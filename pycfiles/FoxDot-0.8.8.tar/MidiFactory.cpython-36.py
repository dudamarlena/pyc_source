# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Ryan\Documents\GitHub\FoxDot\FoxDot\lib\Extensions\VRender\MidiFactory.py
# Compiled at: 2019-01-02 07:34:07
# Size of source mod 2**32: 527 bytes
from midiutil import MIDIFile

def createMidi(midi_file, composition):
    print('Composition:')
    print(composition)
    MyMIDI = MIDIFile(1)
    track = 0
    channel = 0
    for note in composition:
        pitch = note[0]
        duration = note[1]
        volume = note[2]
        time = note[3]
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)

    with open(midi_file, 'wb') as (output_file):
        MyMIDI.writeFile(output_file)