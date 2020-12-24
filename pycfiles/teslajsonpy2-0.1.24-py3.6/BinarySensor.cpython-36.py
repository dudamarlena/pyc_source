# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/BinarySensor.py
# Compiled at: 2018-06-14 16:08:19
# Size of source mod 2**32: 1610 bytes
from teslajsonpy2.vehicle import VehicleDevice

class ParkingSensor(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._ParkingSensor__state = False
        self.type = 'parking brake sensor'
        self.hass_type = 'binary_sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 1
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_drive_params(self._id)
        if data:
            if not data['shift_state'] or data['shift_state'] == 'P':
                self._ParkingSensor__state = True
            else:
                self._ParkingSensor__state = False

    def get_value(self):
        return self._ParkingSensor__state

    @staticmethod
    def has_battery():
        return False


class ChargerConnectionSensor(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._ChargerConnectionSensor__state = False
        self.type = 'charger sensor'
        self.hass_type = 'binary_sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 2

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_charging_params(self._id)
        if data:
            if data['charging_state'] in ('Disconnected', 'Stopped', 'NoPower'):
                self._ChargerConnectionSensor__state = False
            else:
                self._ChargerConnectionSensor__state = True

    def get_value(self):
        return self._ChargerConnectionSensor__state

    @staticmethod
    def has_battery():
        return False