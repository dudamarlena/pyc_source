# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/charger.py
# Compiled at: 2020-04-04 15:06:20
# Size of source mod 2**32: 3508 bytes
"""
Python Package for controlling Subaru API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""
from typing import Dict, Text
import subarulink.const as sc
from subarulink.vehicle import VehicleDevice

class ChargerSwitch(VehicleDevice):
    __doc__ = 'Home-Assistant class for the charger of a Subaru VehicleDevice.'

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._ChargerSwitch__manual_update_time = 0
        self._ChargerSwitch__charger_state = False
        self.type = 'charger switch'
        self.hass_type = 'switch'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 8

    async def async_update(self):
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._ChargerSwitch__charger_state = 'CHARGING' in data['status'][sc.EV_TIME_TO_FULLY_CHARGED]

    async def start_charge(self):
        """Start charging the Subaru Vehicle."""
        if not self._ChargerSwitch__charger_state:
            data = await self._controller.charge_start(self._vin)
            if data:
                if data['data']['success']:
                    self._ChargerSwitch__charger_state = True

    async def stop_charge(self):
        """Stop charging the Subaru Vehicle."""
        if self._ChargerSwitch__charger_state:
            data = await self._controller.charge_stop(self._vin)
            if data:
                if data['data']['success']:
                    self._ChargerSwitch__charger_state = False

    def is_charging(self):
        """Return whether the Subaru Vehicle is charging."""
        return self._ChargerSwitch__charger_state

    @staticmethod
    def has_battery():
        """Return whether the Subaru charger has a battery."""
        return False


class ChargingSensor(VehicleDevice):
    __doc__ = 'Home-Assistant charging sensor class for a Subaru VehicleDevice.'

    def __init__(self, data, controller):
        """Initialize the Charger sensor.

        Args:
            data (Dict): The charging parameters for a Subaru vehicle.
            controller (Controller): The controller that controls updates to the Subaru API.

        """
        super().__init__(data, controller)
        self.type = 'charging rate sensor'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 12
        self._ChargingSensor__time_to_full = 0
        self.measurement = 'LENGTH_MILES'
        self.vin = self._vin

    async def async_update(self):
        """Update the battery state."""
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._ChargingSensor__time_to_full = data['status'][sc.EV_TIME_TO_FULLY_CHARGED]

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    @property
    def time_left(self) -> float:
        """Return the time left to full in hours."""
        return self._ChargingSensor__time_to_full