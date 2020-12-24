# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/data/raw.py
# Compiled at: 2016-07-31 11:56:19
# Size of source mod 2**32: 871 bytes
from .base import BaseType
from .exception import QrDataInvalidException
from ...common import Bits
__all__ = [
 'Raw']

class Raw(BaseType):

    def __init__(self, data, cci_length):
        super().__init__(data, cci_length)

    @property
    def _encoded_data_part(self):
        bits = Bits()
        bits.extend(self.data)
        return bits

    @property
    def _mode_indicator(self):
        return 4

    def _validate(self):
        for i, value in enumerate(self.data):
            if value < 0 or value > 255:
                raise QrDataInvalidException(type(self).__name__, self.data, i)

    @property
    def _encoded_data_part_length(self):
        return 8 * len(self.data)