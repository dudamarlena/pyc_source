# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/Lock.py
# Compiled at: 2018-06-14 16:08:19
# Size of source mod 2**32: 1316 bytes
from teslajsonpy2.vehicle import VehicleDevice
import time

class Lock(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Lock__manual_update_time = 0
        self._Lock__lock_state = False
        self.type = 'door lock'
        self.hass_type = 'lock'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 7
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_state_params(self._id)
        if data:
            if time.time() - self._Lock__manual_update_time > 60:
                self._Lock__lock_state = data['locked']

    def lock(self):
        if not self._Lock__lock_state:
            data = self._controller.command(self._id, 'door_lock')
            if data['response']['result']:
                self._Lock__lock_state = True
            self._Lock__manual_update_time = time.time()

    def unlock(self):
        if self._Lock__lock_state:
            data = self._controller.command(self._id, 'door_unlock')
            if data['response']['result']:
                self._Lock__lock_state = False
            self._Lock__manual_update_time = time.time()

    def is_locked(self):
        return self._Lock__lock_state

    @staticmethod
    def has_battery():
        return False