# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/BinarySensor.py
# Compiled at: 2018-02-18 17:54:30
# Size of source mod 2**32: 3409 bytes
from pyconnectedcars.vehicle import VehicleDevice
import datetime

class SystemsAreOkSensor(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._SystemsAreOkSensor__state = False
        self.lamps = []
        self.indicators = []
        self.last_updated = None
        self.type = 'system ok'
        self.hass_type = 'binary_sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 1
        self.update()

    def update(self):
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            self._SystemsAreOkSensor__state = not data['systemsAreOk']
            self.lamps = data['lamps']
            self.indicators = data['incidents']
            self.last_updated = datetime.datetime.strptime(data['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_value(self):
        return self._SystemsAreOkSensor__state

    @staticmethod
    def has_battery():
        return False


class OilLevelIsOkSensor(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._OilLevelIsOkSensor__state = False
        self.last_updated = None
        self.type = 'oil level'
        self.hass_type = 'binary_sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 1
        self.update()

    def update(self):
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            self._OilLevelIsOkSensor__state = not data['oilLevelIsOk']
            self.last_updated = datetime.datetime.strptime(data['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_value(self):
        return self._OilLevelIsOkSensor__state

    @staticmethod
    def has_battery():
        return False


class TirePressureIsOkSensor(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._TirePressureIsOkSensor__state = False
        self.last_updated = None
        self.type = 'tire pressure'
        self.hass_type = 'binary_sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 1
        self.update()

    def update(self):
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            self._TirePressureIsOkSensor__state = not data['tirePressureIsOk']
            self.last_updated = datetime.datetime.strptime(data['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_value(self):
        return self._TirePressureIsOkSensor__state

    @staticmethod
    def has_battery():
        return False


class BatteryChargeIsOkSensor(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._BatteryChargeIsOkSensor__state = False
        self.last_updated = None
        self.type = 'battery charge'
        self.hass_type = 'binary_sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 1
        self.update()

    def update(self):
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            self._BatteryChargeIsOkSensor__state = not data['batteryChargeIsOk']
            self.last_updated = datetime.datetime.strptime(data['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def get_value(self):
        return self._BatteryChargeIsOkSensor__state

    @staticmethod
    def has_battery():
        return False