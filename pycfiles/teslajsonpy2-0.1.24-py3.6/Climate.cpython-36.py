# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/Climate.py
# Compiled at: 2018-06-14 16:08:19
# Size of source mod 2**32: 3881 bytes
from teslajsonpy2.vehicle import VehicleDevice
import time

class Climate(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Climate__is_auto_conditioning_on = False
        self._Climate__inside_temp = 0
        self._Climate__outside_temp = 0
        self._Climate__driver_temp_setting = 0
        self._Climate__passenger_temp_setting = 0
        self._Climate__is_climate_on = False
        self._Climate__fan_status = 0
        self._Climate__manual_update_time = 0
        self.type = 'HVAC (climate) system'
        self.hass_type = 'climate'
        self.measurement = 'C'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 3
        self.update()

    def is_hvac_enabled(self):
        return self._Climate__is_climate_on

    def get_current_temp(self):
        return self._Climate__inside_temp

    def get_goal_temp(self):
        return self._Climate__driver_temp_setting

    def get_fan_status(self):
        return self._Climate__fan_status

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_climate_params(self._id)
        if data:
            if time.time() - self._Climate__manual_update_time > 60:
                self._Climate__is_auto_conditioning_on = data['is_auto_conditioning_on']
                self._Climate__is_climate_on = data['is_climate_on']
                self._Climate__driver_temp_setting = data['driver_temp_setting'] if data['driver_temp_setting'] else self._Climate__driver_temp_setting
                self._Climate__passenger_temp_setting = data['passenger_temp_setting'] if data['passenger_temp_setting'] else self._Climate__passenger_temp_setting
            self._Climate__inside_temp = data['inside_temp'] if data['inside_temp'] else self._Climate__inside_temp
            self._Climate__outside_temp = data['outside_temp'] if data['outside_temp'] else self._Climate__outside_temp
            self._Climate__fan_status = data['fan_status']

    def set_temperature(self, temp):
        temp = round(temp, 1)
        self._Climate__manual_update_time = time.time()
        data = self._controller.command(self._id, 'set_temps', {'driver_temp':temp,  'passenger_temp':temp})
        if data['response']['result']:
            self._Climate__driver_temp_setting = temp
            self._Climate__passenger_temp_setting = temp

    def set_status(self, enabled):
        self._Climate__manual_update_time = time.time()
        if enabled:
            data = self._controller.command(self._id, 'auto_conditioning_start')
            if data['response']['result']:
                self._Climate__is_auto_conditioning_on = True
                self._Climate__is_climate_on = True
        else:
            data = self._controller.command(self._id, 'auto_conditioning_stop')
        if data['response']['result']:
            self._Climate__is_auto_conditioning_on = False
            self._Climate__is_climate_on = False
        self.update()

    @staticmethod
    def has_battery():
        return False


class TempSensor(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._TempSensor__inside_temp = 0
        self._TempSensor__outside_temp = 0
        self.type = 'temperature sensor'
        self.measurement = 'C'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 4
        self.update()

    def get_inside_temp(self):
        return self._TempSensor__inside_temp

    def get_outside_temp(self):
        return self._TempSensor__outside_temp

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_climate_params(self._id)
        if data:
            self._TempSensor__inside_temp = data['inside_temp'] if data['inside_temp'] else self._TempSensor__inside_temp
            self._TempSensor__outside_temp = data['outside_temp'] if data['outside_temp'] else self._TempSensor__outside_temp

    @staticmethod
    def has_battery():
        return False