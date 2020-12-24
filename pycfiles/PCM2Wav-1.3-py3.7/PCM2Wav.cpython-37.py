# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PCM2Wav/PCM2Wav.py
# Compiled at: 2019-05-02 09:21:09
# Size of source mod 2**32: 2035 bytes
"""
    File name: PCM2Wav.py
    Author: Roel Postelmans
    Date created: 2017
"""
from __future__ import division, print_function
import struct, wave
import PCM.logic as _saleae
import PCM.logic as _sigrok

class PCM2Wav(object):
    __doc__ = '\n        PCM data to Wav converter\n    '
    saleae = _saleae
    sigrok = _sigrok
    analyzers = (saleae, sigrok)
    sample_freq = 48000
    sample_width = 2
    channels = 2
    chunk_size = 256
    _PCM2Wav__formats = {1:'c', 
     2:'h'}
    _PCM2Wav__sample_rates = (16000, 32000, 44100, 48000, 96000, 128000)

    def __init__(self, PCM_parser, csv_file, dst):
        """
            PCM2Wav initialiser
        """
        self.data = PCM_parser(csv_file)
        self._generate(dst)

    def _generate(self, dst):
        """
            The actual conversion
        """
        generating = True
        wav_file = wave.open(dst, 'wb')
        wav_file.setnchannels(self.channels)
        wav_file.setsampwidth(self.sample_width)
        sample_rate = self.data.determine_sample_rate()
        frame_rate = min((self._PCM2Wav__sample_rates), key=(lambda x: abs(x - sample_rate)))
        wav_file.setframerate(frame_rate)
        while generating:
            try:
                channels = [self.data.pop_data()[1] for DISCARD in range(0, self.chunk_size)]
            except EOFError:
                generating = False
                self.data.close()

            frame = self._calc_frame(channels)
            wav_file.writeframes(frame)

        wav_file.close()

    def _chr(self, arg):
        if self.sample_width == 1:
            return chr(arg)
        return arg

    def _sample_2_bin(self, sample):
        return struct.pack(self._PCM2Wav__formats[self.sample_width], self._chr(int(sample)))

    def _calc_frame(self, channels_data):
        return ''.join((self._sample_2_bin(sample) for sample in channels_data))