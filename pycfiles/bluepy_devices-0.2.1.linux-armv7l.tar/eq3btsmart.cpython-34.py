# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/bluepy_devices/devices/eq3btsmart.py
# Compiled at: 2016-04-19 13:08:16
# Size of source mod 2**32: 3346 bytes
"""
Support for eq3 Bluetooth Smart thermostats.

All temperatures in Celsius.

To get the current state, update() has to be called for powersaving reasons.
"""
import struct
from datetime import datetime
from ..lib.connection import BTLEConnection
PROP_WRITE_HANDLE = 1041
PROP_NTFY_HANDLE = 1057
PROP_ID_QUERY = 0
PROP_ID_RETURN = 1
PROP_INFO_QUERY = 3
PROP_INFO_RETURN = 2
PROP_SCHEDULE_QUERY = 32
PROP_SCHEDULE_RETURN = 33
PROP_TEMPERATURE_WRITE = 65

class EQ3BTSmartThermostat:
    __doc__ = 'Representation of a EQ3 Bluetooth Smart thermostat.'

    def __init__(self, _mac):
        """Initialize the thermostat."""
        self._target_temperature = -1
        self._mode = -1
        self._conn = BTLEConnection(_mac)
        self._conn.set_callback(PROP_NTFY_HANDLE, self.handle_notification)
        self._conn.connect()
        self._set_time()
        self.update()

    def __str__(self):
        return 'MAC: ' + self._conn.mac + ' Mode: ' + str(self.mode) + ' = ' + self.mode_readable + ' T: ' + str(self.target_temperature)

    def handle_notification(self, data):
        """Handle Callback from a Bluetooth (GATT) request."""
        if data[0] == PROP_INFO_RETURN:
            self._mode = data[2] & 1
            self._target_temperature = data[5] / 2.0

    def _set_time(self):
        """Set the correct time into the thermostat."""
        time = datetime.now()
        value = struct.pack('BBBBBB', int(time.strftime('%y')), time.month, time.day, time.hour, time.minute, time.second)
        self._conn.write_command_raw(PROP_WRITE_HANDLE, value)

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @target_temperature.setter
    def target_temperature(self, temperature):
        """Set new target temperature."""
        value = struct.pack('BB', PROP_TEMPERATURE_WRITE, int(temperature * 2))
        self._conn.write_request_raw(PROP_WRITE_HANDLE, value)

    @property
    def mode(self):
        """Return the mode (auto / manual)."""
        return self._mode

    @property
    def mode_readable(self):
        """Return a readable representation of the mode.."""
        return self.decode_mode(self._mode)

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 4.5

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 30.5

    def pack_byte(self, byte):
        """Pack a byte."""
        return self._conn.pack_byte(byte)

    @staticmethod
    def decode_mode(mode):
        """Convert the numerical mode to a human-readable description."""
        ret = ''
        if mode & 1:
            ret = 'manual'
        else:
            ret = 'auto'
        if mode & 2:
            ret = ret + ' holiday'
        if mode & 4:
            ret = ret + ' boost'
        if mode & 8:
            ret = ret + ' dst'
        if mode & 16:
            ret = ret + ' window'
        return ret

    def update(self):
        """Update the data from the thermostat."""
        self._conn.write_request_raw(PROP_WRITE_HANDLE, self.pack_byte(PROP_INFO_QUERY))