# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/BatterySensor.py
# Compiled at: 2018-06-14 16:07:13
# Size of source mod 2**32: 2246 bytes
from teslajsonpy2.vehicle import VehicleDevice

class Battery(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Battery__battery_level = 0
        self._Battery__charging_state = None
        self._Battery__charge_port_door_open = None
        self.type = 'battery sensor'
        self.measurement = '%'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 5
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_charging_params(self._id)
        if data:
            self._Battery__battery_level = data['battery_level']
            self._Battery__charging_state = data['charging_state']

    @staticmethod
    def has_battery():
        return False

    def get_value(self):
        return self._Battery__battery_level


class Range(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Range__battery_range = 0
        self._Range__est_battery_range = 0
        self._Range__ideal_battery_range = 0
        self.type = 'range sensor'
        self._Range__rated = True
        self.measurement = 'LENGTH_MILES'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 10
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_charging_params(self._id)
        if data:
            self._Range__battery_range = data['battery_range']
            self._Range__est_battery_range = data['est_battery_range']
            self._Range__ideal_battery_range = data['ideal_battery_range']
        data = self._controller.get_gui_params(self._id)
        if data:
            if data['gui_distance_units'] == 'mi/hr':
                self.measurement = 'LENGTH_MILES'
            else:
                self.measurement = 'LENGTH_KILOMETERS'
            self._Range__rated = data['gui_range_display'] == 'Rated'

    @staticmethod
    def has_battery():
        return False

    def get_value(self):
        if self._Range__rated:
            return self._Range__battery_range
        else:
            return self._Range__ideal_battery_range