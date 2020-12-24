# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/bluepy_devices/lib/connection.py
# Compiled at: 2016-04-19 08:17:56
# Size of source mod 2**32: 3025 bytes
"""
Handles Connection duties (reconnecting etc.) transparently.
"""
import logging, struct
from bluepy import btle
REQUIREMENTS = [
 'bluepy>=1.0.4']
DEFAULT_TIMEOUT = 1
_LOGGER = logging.getLogger(__name__)

class BTLEConnection(btle.DefaultDelegate):
    __doc__ = 'Representation of a BTLE Connection.'

    def __init__(self, mac):
        """Initialize the connection."""
        btle.DefaultDelegate.__init__(self)
        self._mac = mac
        self._conn = btle.Peripheral()
        self._callback = {}

    def __del__(self):
        """Destructor - make sure the connection is disconnected."""
        self.disconnect()

    def handleNotification(self, handle, data):
        """Handle Callback from a Bluetooth (GATT) request."""
        if handle in self._callback:
            self._callback[handle](data)

    def connect(self, error=False):
        """Connect to the Bluetooth thermostat."""
        _LOGGER.info('BTLEConnection: connecting to ' + self._mac)
        try:
            self._conn.connect(self._mac)
            self._conn.withDelegate(self)
        except btle.BTLEException:
            if error:
                raise
            else:
                self.disconnect()
                self.connect(True)

    def disconnect(self):
        """Close the Bluetooth connection."""
        self._conn.disconnect()

    @property
    def mac(self):
        """Return the MAC address of the connected device."""
        return self._mac

    def set_callback(self, handle, function):
        """Set the callback for a Notification handle. It will be called with the parameter data, which is binary."""
        self._callback[handle] = function

    def write_request(self, handle, value, timeout=DEFAULT_TIMEOUT):
        """Write a GATT Command with callback."""
        self.write_command(handle, value, timeout, True)

    def write_request_raw(self, handle, value, timeout=DEFAULT_TIMEOUT):
        """Write a GATT Command with callback - no utf-8."""
        self.write_command_raw(handle, value, timeout, True)

    def write_command(self, handle, value, timeout=DEFAULT_TIMEOUT, wait_for_it=False):
        """Write a GATT Command without callback."""
        self.write_command_raw(handle, value.encode('utf-8'), timeout, wait_for_it)

    def write_command_raw(self, handle, value, timeout=DEFAULT_TIMEOUT, wait_for_it=False, exception=False):
        """Write a GATT Command without callback - not utf-8."""
        try:
            self._conn.writeCharacteristic(handle, value, wait_for_it)
            if wait_for_it:
                while self._conn.waitForNotifications(timeout):
                    continue

        except btle.BTLEException:
            if exception is False:
                self.disconnect()
                self.connect()
                self.write_command_raw(handle, value, wait_for_it, True)

    @staticmethod
    def pack_byte(byte):
        """Pack a byte."""
        return struct.pack('B', byte)