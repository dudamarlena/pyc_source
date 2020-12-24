# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Joseph\PycharmProjects\pyformulas\_formulas\audio\play.py
# Compiled at: 2018-05-22 19:39:42
# Size of source mod 2**32: 1365 bytes
import pyaudio

class play:

    def __init__(self, wavedata, bitrate=None, duration=None, num_channels=1, bit_depth=16, block=False):
        import pyformulas as pf
        self.wavedata = wavedata if isinstance(wavedata, bytes) or isinstance(wavedata, bytearray) else bytes(wavedata)
        self.bitrate = bitrate
        self.duration = duration
        self.num_channels = num_channels
        formats = {8:pyaudio.paInt8, 
         16:pyaudio.paInt16,  24:pyaudio.paInt24,  32:pyaudio.paInt32}
        self.format = formats[bit_depth]
        if not len(wavedata) % (bit_depth / 8 * num_channels) == 0:
            raise AssertionError
        else:
            if block:
                self._play()
            else:
                pf.thread(self._play)

    def _play(self):
        pa = pyaudio.PyAudio()
        if self.bitrate is None:
            if self.duration is None:
                raise ValueError('Must set either bitrate or duration')
        if self.duration is not None:
            bits = len(self.wavedata) * 8
            self.bitrate = bits / self.duration
        sample_rate = round(self.bitrate / 8)
        stream = pa.open(format=(self.format),
          channels=(self.num_channels),
          rate=sample_rate,
          output=True)
        stream.write(self.wavedata)
        stream.stop_stream()
        stream.close()
        pa.terminate()