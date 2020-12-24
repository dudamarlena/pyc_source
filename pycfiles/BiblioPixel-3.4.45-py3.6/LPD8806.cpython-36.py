# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/SPI/LPD8806.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 755 bytes
from ...colors import gamma
from ..channel_order import ChannelOrder
from .base import SPIBase

class LPD8806(SPIBase):
    __doc__ = 'Main driver for LPD8806 based LED strips on devices like the Raspberry Pi\n       and BeagleBone.\n\n    Provides the same parameters as\n    :py:class:`bibliopixel.drivers.SPI.SPIBase`\n    '

    def __init__(self, num, gamma=gamma.LPD8806, **kwargs):
        (super().__init__)(num, gamma=gamma, **kwargs)
        self._latchBytes = (self.numLEDs + 31) // 32
        for i in range(0, self._latchBytes):
            self._buf.append(0)