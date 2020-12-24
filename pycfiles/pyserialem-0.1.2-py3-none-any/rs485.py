# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/rs485.py
# Compiled at: 2015-08-29 22:44:26
__doc__ = 'The settings for RS485 are stored in a dedicated object that can be applied to\nserial ports (where supported).\nNOTE: Some implementations may only support a subset of the settings.\n'
import time, serial

class RS485Settings(object):

    def __init__(self, rts_level_for_tx=True, rts_level_for_rx=False, loopback=False, delay_before_tx=None, delay_before_rx=None):
        self.rts_level_for_tx = rts_level_for_tx
        self.rts_level_for_rx = rts_level_for_rx
        self.loopback = loopback
        self.delay_before_tx = delay_before_tx
        self.delay_before_rx = delay_before_rx


class RS485(serial.Serial):
    """    A subclass that replaces the write method with one that toggles RTS
    according to the RS485 settings.

    NOTE: This may work unreliably on some serial ports (control signals not
          synchronized or delayed compared to data). Using delays may be
          unreliable (varying times, larger than expected) as the OS may not
          support very fine grained delays (no smaller than in the order of
          tens of milliseconds).

    NOTE: Some implementations support this natively. Better performance
          can be expected when the native version is used.

    NOTE: The loopback property is ignored by this implementation. The actual
          behavior depends on the used hardware.

    Usage:

        ser = RS485(...)
        ser.rs485_mode = RS485Settings(...)
        ser.write(b'hello')
    """

    def __init__(self, *args, **kwargs):
        super(RS485, self).__init__(*args, **kwargs)
        self._alternate_rs485_settings = None
        return

    def write(self, b):
        """Write to port, controlling RTS before and after transmitting."""
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
        return

    @property
    def rs485_mode(self):
        """        Enable RS485 mode and apply new settings, set to None to disable.
        See serial.rs485.RS485Settings for more info about the value.
        """
        return self._alternate_rs485_settings

    @rs485_mode.setter
    def rs485_mode(self, rs485_settings):
        self._alternate_rs485_settings = rs485_settings