# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\serial\rs485.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 3265 bytes
"""The settings for RS485 are stored in a dedicated object that can be applied to
serial ports (where supported).
NOTE: Some implementations may only support a subset of the settings.
"""
import time, serial

class RS485Settings(object):

    def __init__(self, rts_level_for_tx=True, rts_level_for_rx=False, loopback=False, delay_before_tx=None, delay_before_rx=None):
        self.rts_level_for_tx = rts_level_for_tx
        self.rts_level_for_rx = rts_level_for_rx
        self.loopback = loopback
        self.delay_before_tx = delay_before_tx
        self.delay_before_rx = delay_before_rx


class RS485(serial.Serial):
    __doc__ = "    A subclass that replaces the write method with one that toggles RTS\n    according to the RS485 settings.\n\n    NOTE: This may work unreliably on some serial ports (control signals not\n          synchronized or delayed compared to data). Using delays may be\n          unreliable (varying times, larger than expected) as the OS may not\n          support very fine grained delays (no smaller than in the order of\n          tens of milliseconds).\n\n    NOTE: Some implementations support this natively. Better performance\n          can be expected when the native version is used.\n\n    NOTE: The loopback property is ignored by this implementation. The actual\n          behavior depends on the used hardware.\n\n    Usage:\n\n        ser = RS485(...)\n        ser.rs485_mode = RS485Settings(...)\n        ser.write(b'hello')\n    "

    def __init__(self, *args, **kwargs):
        (super(RS485, self).__init__)(*args, **kwargs)
        self._alternate_rs485_settings = None

    def write(self, b):
        if self._alternate_rs485_settings is not None:
            self.setRTS(self._alternate_rs485_settings.rts_level_for_tx)
            if self._alternate_rs485_settings.delay_before_tx is not None:
                time.sleep(self._alternate_rs485_settings.delay_before_tx)
            super(RS485, self).write(b)
            super(RS485, self).flush()
            if self._alternate_rs485_settings.delay_before_rx is not None:
                time.sleep(self._alternate_rs485_settings.delay_before_rx)
            self.setRTS(self._alternate_rs485_settings.rts_level_for_rx)
        else:
            super(RS485, self).write(b)

    @property
    def rs485_mode(self):
        """        Enable RS485 mode and apply new settings, set to None to disable.
        See serial.rs485.RS485Settings for more info about the value.
        """
        return self._alternate_rs485_settings

    @rs485_mode.setter
    def rs485_mode(self, rs485_settings):
        self._alternate_rs485_settings = rs485_settings