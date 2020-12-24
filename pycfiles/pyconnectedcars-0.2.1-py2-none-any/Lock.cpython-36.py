# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/Lock.py
# Compiled at: 2018-02-18 16:25:19
# Size of source mod 2**32: 954 bytes
from pyconnectedcars.vehicle import VehicleDevice
import datetime

class Lock(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Lock__lock_state = False
        self.last_updated = 0
        self.type = 'door lock'
        self.hass_type = 'lock'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 7
        self.update()

    def update(self):
        self._controller.update()
        data = self._controller.get_car_params(self._id)
        if data:
            if data['lockedState'] == 'UNLOCKED':
                self._Lock__lock_state = False
            else:
                self._Lock__lock_state = True
            self.last_updated = datetime.datetime.strptime(data['lockedStateUpdatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    def is_locked(self):
        return self._Lock__lock_state

    @staticmethod
    def has_battery():
        return False