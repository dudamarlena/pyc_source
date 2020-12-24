# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/SPI/WS2801.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 643 bytes
from ..channel_order import ChannelOrder
from .base import SPIBase
from ...colors import gamma
SPI_SPEED_ERROR = 'WS2801 requires an SPI speed of 1MHz but was set to {}MHz'

class WS2801(SPIBase):
    __doc__ = 'Main driver for WS2801 based LED strips on devices like the\n    Raspberry Pi and BeagleBone\n\n    Provides the same parameters as\n    :py:class:`bibliopixel.drivers.SPI.SPIBase`\n    '

    def __init__(self, num, gamma=gamma.WS2801, spi_speed=1, **kwargs):
        if not 0 < spi_speed <= 1:
            raise ValueError(SPI_SPEED_ERROR.format(spi_speed))
        (super().__init__)(num, gamma=gamma, spi_speed=spi_speed, **kwargs)