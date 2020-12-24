# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/Fuel.py
# Compiled at: 2018-02-18 17:42:35
# Size of source mod 2**32: 982 bytes
from pyconnectedcars.vehicle import VehicleDevice
import datetime

class Fuel(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Fuel__fuel_level = 0
        self.fuel_level_pct = 0
        self.last_updated = 0
        self.type = 'fuel level'
        self.measurement = 'VOLUME_LITERS'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 5
        self.update()

    def update(self):
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            self._Fuel__fuel_level = data['fuelLevelLiter']
            self.fuel_level_pct = data['fuelLevel']
            self.last_updated = datetime.datetime.strptime(data['fuelLevelUpdatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def has_battery():
        return False

    def get_value(self):
        return self._Fuel__fuel_level