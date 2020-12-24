# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/climate.py
# Compiled at: 2020-04-04 15:06:20
# Size of source mod 2**32: 5565 bytes
"""
Python Package for controlling Subaru API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""
import time
import subarulink.const as sc
from subarulink.vehicle import VehicleDevice

class Climate(VehicleDevice):
    __doc__ = 'Home-assistant class of HVAC for Subaru vehicles.\n\n    This is intended to be partially inherited by a Home-Assitant entity.\n    '

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Climate__temp_setting = 72
        self._Climate__fan_setting = sc.FAN_SPEED_MED
        self._Climate__mode = sc.MODE_SPLIT
        self._Climate__rear_defrost = sc.REAR_DEFROST_OFF
        self._Climate__rear_ac = sc.REAR_AC_OFF
        self._Climate__recirculate = sc.RECIRCULATE_OFF
        self._Climate__left_seat = sc.HEAT_SEAT_OFF
        self._Climate__right_seat = sc.HEAT_SEAT_OFF
        self._Climate__is_climate_on = False
        self._Climate__start_time = None
        self._Climate__duration = 600
        self._Climate__manual_update_time = time.time()
        self.type = 'HVAC (climate) system'
        self.hass_type = 'climate'
        self.measurement = 'F'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 3

    def is_hvac_enabled(self):
        """Return whether HVAC is running."""
        if self._Climate__start_time:
            if time.time() - self._Climate__start_time >= self._Climate__duration:
                return False
            return True
        return False

    def get_goal_temp(self):
        """Return driver set temperature."""
        return self._Climate__temp_setting

    def get_fan_setting(self):
        """Return fan status."""
        return self._Climate__fan_setting

    def get_mode(self):
        """Return HVAC mode."""
        return self._Climate__mode

    async def async_update(self):
        await super().async_update()

    async def set_temperature(self, temp):
        """Set HVAC target temperature."""
        self._Climate__temp_setting = temp

    async def set_status(self, enabled):
        """Enable or disable the HVAC."""
        self._Climate__manual_update_time = time.time()
        if enabled:
            await self._controller.remote_start(self._vin, self._Climate__temp_setting, self._Climate__mode, self._Climate__left_seat, self._Climate__right_seat, self._Climate__rear_defrost, self._Climate__fan_setting, self._Climate__recirculate, self._Climate__rear_ac)
            self._Climate__start_time = time.time()
        else:
            await self._controller.remote_stop(self._vin)

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class TempSensor(VehicleDevice):
    __doc__ = 'Home-assistant class of temperature sensors for Subaru vehicles.\n\n    This is intended to be partially inherited by a Home-Assitant entity.\n    '

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._TempSensor__outside_temp = 0
        self.type = 'External Temp'
        self.measurement = 'F'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 4

    def get_outside_temp(self):
        """Get outside temperature."""
        return self._TempSensor__outside_temp

    async def async_update(self):
        await super().async_update()
        data = await self._controller.get_data(self._vin)
        if data:
            self._TempSensor__outside_temp = float(data['status'][sc.EXTERNAL_TEMP])

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False