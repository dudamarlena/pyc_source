# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/battery_sensor.py
# Compiled at: 2020-04-12 13:47:40
# Size of source mod 2**32: 3030 bytes
"""
subarulink - A Python Package for interacting with Subaru Starlink Remote Services API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""
from typing import Dict, Text
import subarulink.const as sc
from subarulink.vehicle import VehicleDevice

class Battery(VehicleDevice):
    __doc__ = 'Home-Assistant battery class for a Subaru VehicleDevice.'

    def __init__(self, data, controller):
        """Initialize the Battery sensor.

        Args:
            data (Dict): The charging parameters for a Subaru vehicle.
            controller (Controller): The controller that controls updates to the Subaru API.

        """
        super().__init__(data, controller)
        self._Battery__battery_level = 0
        self._Battery__charging_state = None
        self.type = 'battery sensor'
        self.measurement = '%'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 5

    async def async_update(self):
        """Update the battery state."""
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._Battery__battery_level = data['status'][sc.EV_STATE_OF_CHARGE_PERCENT]
            self._Battery__charging_state = data['status'][sc.EV_CHARGER_STATE_TYPE]

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    def get_value(self) -> int:
        """Return the battery level."""
        return self._Battery__battery_level


class Range(VehicleDevice):
    __doc__ = 'Home-Assistant class of the battery range for a Subaru VehicleDevice.'

    def __init__(self, data, controller):
        """Initialize the Battery range sensor.

        Parameters
        ----------
        data : dict
            The charging parameters for a Subaru vehicle.
            https://tesla-api.timdorr.com/vehicle/state/chargestate
        controller : subarulink.Controller
            The controller that controls updates to the Subaru API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self._Range__battery_range = 0
        self.type = 'EV Range'
        self.measurement = 'LENGTH_MILES'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 10

    async def async_update(self):
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._Range__battery_range = data['status'][sc.EV_DISTANCE_TO_EMPTY]

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False

    def get_value(self):
        """Return the battery range."""
        return self._Range__battery_range