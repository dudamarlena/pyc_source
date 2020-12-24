# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PCM2Wav/PCM/logic/sigrok.py
# Compiled at: 2019-05-02 09:23:01
# Size of source mod 2**32: 2300 bytes
"""
    File name: PCM.py
    Author: Roel Postelmans
    Date created: 2017
"""
from ..PCM import PCM

class I2S(PCM):
    __doc__ = '\n        I2S data parser for sigrok protocol decoders\n\n        format example:\n        ...\n        Left channel: 00010000\n        Right channel: 00260000\n        Left channel: 00010000\n        Right channel: 00270000\n        ...\n\n    '
    VALUE_LOC = -1
    CHANNEL_LOC = 0
    FIRST_D = 0
    sample_rate = None
    line = None

    def __init__(self, csv_file, delimiter=' '):
        """
            Sigrok I2S export parser initiator
        """
        super(I2S, self).__init__(csv_file, self.FIRST_D)
        self.delimiter = delimiter

    def extract_value(self, line, key):
        """
            Extract a value from a string by a given position
        """
        line = line.split(self.delimiter)
        line = line[key].rstrip()
        return line

    def determine_sample_rate(self):
        if self.sample_rate is None:
            raise ValueError("Sigrok export doesn't contain timestamps,you have to set sigrok.sample_rate")
        super(I2S, self).reset()
        return self.sample_rate

    def pop_data(self):
        d_channel = {'Left':0, 
         'Right':1}
        if self.line is None:
            super(I2S, self).pop_data()
            value = self.extract_value(self.line, self.VALUE_LOC)[:4]
            channel = self.extract_value(self.line, self.CHANNEL_LOC)
        else:
            value = self.extract_value(self.line, self.VALUE_LOC)[4:]
            channel = self.extract_value(self.line, self.CHANNEL_LOC)
            self.line = None
        value = int(value, 16)
        if value & 32768 == 32768:
            value = -((value ^ 65535) + 1)
        return (
         d_channel[channel], value)

    def close(self):
        self.sample_count -= self.FIRST_D
        super(I2S, self).close()