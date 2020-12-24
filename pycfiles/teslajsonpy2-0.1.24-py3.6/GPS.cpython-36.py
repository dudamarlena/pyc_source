# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/GPS.py
# Compiled at: 2018-06-14 16:08:19
# Size of source mod 2**32: 2242 bytes
from teslajsonpy2.vehicle import VehicleDevice

class GPS(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._GPS__longitude = 0
        self._GPS__latitude = 0
        self._GPS__heading = 0
        self._GPS__location = {}
        self.last_seen = 0
        self.last_updated = 0
        self.type = 'location tracker'
        self.hass_type = 'devices_tracker'
        self.bin_type = 6
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.update()

    def get_location(self):
        return self._GPS__location

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_drive_params(self._id)
        if data:
            self._GPS__longitude = data['longitude']
            self._GPS__latitude = data['latitude']
            self._GPS__heading = data['heading']
        if self._GPS__longitude:
            if self._GPS__latitude:
                if self._GPS__heading:
                    self._GPS__location = {'longitude':self._GPS__longitude, 
                     'latitude':self._GPS__latitude, 
                     'heading':self._GPS__heading}

    @staticmethod
    def has_battery():
        return False


class Odometer(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Odometer__odometer = 0
        self.type = 'mileage sensor'
        self.measurement = 'LENGTH_MILES'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 11
        self.update()
        self._Odometer__rated = True

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_state_params(self._id)
        if data:
            self._Odometer__odometer = data['odometer']
        data = self._controller.get_gui_params(self._id)
        if data:
            if data['gui_distance_units'] == 'mi/hr':
                self.measurement = 'LENGTH_MILES'
            else:
                self.measurement = 'LENGTH_KILOMETERS'
            self._Odometer__rated = data['gui_range_display'] == 'Rated'

    @staticmethod
    def has_battery():
        return False

    def get_value(self):
        return round(self._Odometer__odometer, 1)