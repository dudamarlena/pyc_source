# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/SPI/WS281X.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1823 bytes
from ..channel_order import ChannelOrder
from .base import SPIBase
from ...colors import gamma as _gamma
from . import interfaces
MAX_PIXELS = 455

class WS281X(SPIBase):
    __doc__ = '\n    SPI driver for WS2812(b) based LED strips on devices like\n    Raspberry Pi, OrangePi, BeagleBone,..\n\n    Provides the same parameters as\n    :py:class:`bibliopixel.drivers.SPI.SPIBase`\n    '

    def __init__(self, num, gamma=_gamma.WS2812, spi_speed=3.2, **kwargs):
        (super().__init__)(num, gamma=gamma, spi_speed=spi_speed, **kwargs)
        if isinstance(self._interface, interfaces.SpiFileInterface):
            raise ValueError('SPI File interface is unsupported by WS281X')
        if num > MAX_PIXELS:
            raise ValueError('WS2812X SPI driver only supports {} pixels max.'.format(MAX_PIXELS))

    def _compute_packet(self):
        super()._compute_packet()
        buf2 = bytearray([0])
        for byte in self._buf:
            tmp = 0
            for i in range(8):
                tmp |= (4 | (2 if byte & 1 << i > 0 else 0)) << i * 3

            buf2.append(tmp >> 16 & 255)
            buf2.append(tmp >> 8 & 255)
            buf2.append(tmp & 255)

        self._packet = buf2