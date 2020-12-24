# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/media/CreateDialTone.py
# Compiled at: 2016-08-01 11:57:45


def generate_dial_tone(filename='dialtone.wav', volume=50):
    import math, wave, array
    duration = 3
    freq = 440
    data = array.array('h')
    sampleRate = 44100
    numChan = 1
    dataSize = 2
    numSamplesPerCyc = int(sampleRate / freq)
    numSamples = sampleRate * duration
    for i in range(numSamples / 2):
        sample = 32767 * float(volume) / 100
        sample *= math.sin(math.pi * 2 * (i % numSamplesPerCyc) / numSamplesPerCyc)
        data.append(int(sample))

    for i in range(numSamples / 2):
        sample = 0
        data.append(int(sample))

    f = wave.open(filename, 'w')
    f.setparams((numChan, dataSize, sampleRate, numSamples, 'NONE', 'Uncompressed'))
    f.writeframes(data.tostring())
    f.close()
    return filename