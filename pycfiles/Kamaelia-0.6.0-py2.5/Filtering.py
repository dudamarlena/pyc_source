# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Audio/Filtering.py
# Compiled at: 2008-10-19 12:19:52
from Axon.Component import component

class LPF(component):
    """Low pass butterworth filter for 8Hz data. One pole, -3dB at 2KHz"""

    def filtering(self, data):
        output = []
        prevsample = self.prevsample
        prevout = self.prevout
        GAIN = 3.4142136
        PREVSCALER = 0.4142136
        for sample in data:
            sample = sample / GAIN
            out = sample + prevsample + PREVSCALER * prevout
            output.append(out)
            prevsample = sample
            prevout = out

        self.prevsample = prevsample
        self.prevout = prevout
        return output

    def main(self):
        self.prevsample = 0
        self.prevout = 0
        while 1:
            while self.dataReady('inbox'):
                rawdata = self.recv('inbox')
                filtered = convertback(self.filtering(convert(rawdata)))
                self.send(filtered, 'outbox')

            self.pause()
            yield 1


def convert(data):
    converted = []
    for i in xrange(0, len(data), 2):
        value = ord(data[i]) + (ord(data[(i + 1)]) << 8)
        if value & 32768:
            value -= 65536
        converted.append(value)

    return converted


def convertback(data):
    output = []
    for sample in data:
        sample = int(sample)
        output.append(chr(sample & 255) + chr(sample >> 8 & 255))

    return ('').join(output)


__kamaelia_components__ = (
 LPF,)
if __name__ == '__main__':
    import sys
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.Audio.PyMedia.Input import Input
    from Kamaelia.Audio.PyMedia.Output import Output
    from Kamaelia.Codec.Speex import SpeexEncode, SpeexDecode
    from Kamaelia.Audio.RawAudioMixer import RawAudioMixer
    sys.path.append('../../Tools/Whiteboard/Whiteboard')
    from Entuple import Entuple
    Pipeline(Input(sample_rate=8000, channels=1, format='S16_LE'), LPF(), SpeexEncode(3), SpeexDecode(3), Entuple(prefix=['A'], postfix=[]), RawAudioMixer(), Output(sample_rate=8000, channels=1, format='S16_LE')).run()