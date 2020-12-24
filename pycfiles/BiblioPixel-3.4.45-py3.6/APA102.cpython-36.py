# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/SPI/APA102.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2252 bytes
from ...colors import gamma
from ..channel_order import ChannelOrder
from .base import SPIBase

class APA102(SPIBase):
    __doc__ = 'Driver for APA102/SK9822 based LED strips on devices like\n    the Raspberry Pi and BeagleBone\n\n    Provides the same parameters as\n    :py:class:`bibliopixel.drivers.SPI.SPIBase`\n    '

    def __init__(self, num, gamma=gamma.APA102, **kwargs):
        (super().__init__)(num, gamma=gamma, **kwargs)
        self._start_frame = 4
        self._pixel_bytes = self.numLEDs * 4
        self._pixel_stop = self._start_frame + self._pixel_bytes
        self._reset_frame = 4
        self._end_frame = num // 2 + 1
        self._packet = self.maker.bytes(self._start_frame + self._pixel_bytes + self._reset_frame + self._end_frame)
        self.set_device_brightness(255)

    def set_device_brightness(self, val):
        """
        APA102 & SK9822 support on-chip brightness control, allowing greater
        color depth.

        APA102 superimposes a 440Hz PWM on the 19kHz base PWM to control
        brightness. SK9822 uses a base 4.7kHz PWM but controls brightness with a
        variable current source.

        Because of this SK9822 will have much less flicker at lower levels.
        Either way, this option is better and faster than scaling in
        BiblioPixel.
        """
        self._chipset_brightness = val >> 3
        self._brightness_list = [224 + self._chipset_brightness] * self.numLEDs
        self._packet[self._start_frame:self._pixel_stop:4] = self._brightness_list

    def _compute_packet(self):
        self._render()
        self._packet[self._start_frame + 1:self._pixel_stop:4] = self._buf[0::3]
        self._packet[self._start_frame + 2:self._pixel_stop:4] = self._buf[1::3]
        self._packet[self._start_frame + 3:self._pixel_stop:4] = self._buf[2::3]