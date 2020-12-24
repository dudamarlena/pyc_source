# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/GPS.py
# Compiled at: 2018-02-18 17:41:55
# Size of source mod 2**32: 1999 bytes
from pyconnectedcars.vehicle import VehicleDevice
import datetime

class GPS(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._GPS__longitude = 0
        self._GPS__latitude = 0
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
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            self._GPS__longitude = data['long']
            self._GPS__latitude = data['lat']
            self.last_updated = datetime.datetime.strptime(data['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if self._GPS__longitude:
            if self._GPS__latitude:
                self._GPS__location = {'longitude':self._GPS__longitude, 
                 'latitude':self._GPS__latitude}

    @staticmethod
    def has_battery():
        return False


class Odometer(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Odometer__odometer = 0
        self.last_updated = 0
        self.type = 'mileage'
        self.measurement = 'LENGTH_KILOMETERS'
        self.hass_type = 'sensor'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 11
        self.update()
        self._Odometer__rated = True

    def update(self):
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            self._Odometer__odometer = data['odometer']
            self.last_updated = datetime.datetime.strptime(data['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def has_battery():
        return False

    def get_value(self):
        return round(self._Odometer__odometer, 1)