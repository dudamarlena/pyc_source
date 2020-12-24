# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/binary_sensor.py
# Compiled at: 2020-04-04 15:05:19
# Size of source mod 2**32: 1666 bytes
"""
Python Package for controlling Subaru API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""
import subarulink.const as sc
from subarulink.vehicle import VehicleDevice

class ChargerConnectionSensor(VehicleDevice):
    __doc__ = 'Home-assistant charger connection class for Subaru vehicles.\n\n    This is intended to be partially inherited by a Home-Assitant entity.\n    '

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._ChargerConnectionSensor__state = False
        self.type = 'charger sensor'
        self.hass_type = 'binary_sensor'
        self.name = self._name()
        self.sensor_type = 'connectivity'
        self.uniq_name = self._uniq_name()
        self.bin_type = 2

    async def async_update(self):
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._ChargerConnectionSensor__state = 'LOCKED_CONNECTED' in data['status'][sc.EV_IS_PLUGGED_IN]

    def get_value(self):
        """Return whether the charger cable is connected."""
        return self._ChargerConnectionSensor__state

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False