# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/gps.py
# Compiled at: 2020-04-04 15:06:20
# Size of source mod 2**32: 3426 bytes
"""
Python Package for controlling Subaru API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""
import subarulink.const as sc
from subarulink.vehicle import VehicleDevice

class GPS(VehicleDevice):
    __doc__ = 'Home-assistant class for GPS of Subaru vehicles.'

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._GPS__longitude = 0
        self._GPS__latitude = 0
        self._GPS__heading = 0
        self._GPS__speed = 0
        self._GPS__location = None
        self.last_seen = 0
        self.last_updated = 0
        self.type = 'location tracker'
        self.hass_type = 'devices_tracker'
        self.bin_type = 6
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    def get_location(self):
        """Return the current location."""
        return self._GPS__location

    async def async_update(self):
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._GPS__longitude = data['location'][sc.LONGITUDE]
            self._GPS__latitude = data['location'][sc.LATITUDE]
            self._GPS__heading = data['location'][sc.HEADING]
            self._GPS__speed = data['location'][sc.SPEED]
        if self._GPS__longitude:
            if self._GPS__latitude:
                self._GPS__location = {'longitude':self._GPS__longitude, 
                 'latitude':self._GPS__latitude, 
                 'heading':self._GPS__heading, 
                 'speed':self._GPS__speed}

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class Odometer(VehicleDevice):
    __doc__ = 'Home-assistant class for odometer of Subaru vehicles.'

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Odometer__odometer = 0
        self.type = 'Odometer'
        self.measurement = 'LENGTH_MILES'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 11
        self._Odometer__rated = True

    async def async_update(self):
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._Odometer__odometer = data['status'][sc.ODOMETER]

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False

    def get_value(self):
        """Return the odometer reading."""
        return self._Odometer__odometer