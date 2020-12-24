# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/data/numbers.py
# Compiled at: 2016-07-31 11:56:28
# Size of source mod 2**32: 1004 bytes
from .base import BaseType
from ...common import Bits
from .exception import QrDataInvalidException

class Numbers(BaseType):

    def __init__(self, data, cci_length):
        super().__init__(data, cci_length)

    def _validate(self):
        for i, value in enumerate(self.data):
            if not ord('0') <= ord(value) <= ord('9'):
                raise QrDataInvalidException(type(self).__name__, self.data, i)

    @property
    def _encoded_data_part(self):
        bits = Bits()
        split = (self.data[x:x + 3] for x in range(0, len(self.data), 3))
        for i, string in enumerate(split):
            bits.append(int(string), 1 + 3 * len(string))

        return bits

    @property
    def _mode_indicator(self):
        return 1

    @property
    def _encoded_data_part_length(self):
        return 10 * (len(self.data) // 3) + [0, 4, 7][(len(self.data) % 3)]