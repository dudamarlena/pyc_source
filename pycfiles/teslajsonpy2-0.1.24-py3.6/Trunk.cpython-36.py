# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/teslajsonpy2/Trunk.py
# Compiled at: 2018-06-14 16:56:39
# Size of source mod 2**32: 2234 bytes
from teslajsonpy2.vehicle import VehicleDevice
import time

class FrontTrunk(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._FrontTrunk__manual_update_time = 0
        self._FrontTrunk__front_trunk_state = False
        self.type = 'front trunk lock'
        self.hass_type = 'lock'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 12
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_vehicle_params(self._id)
        if data:
            if time.time() - self._FrontTrunk__manual_update_time > 60:
                self._FrontTrunk__front_trunk_state = data['ft']

    def open_front_trunk(self):
        if not self._FrontTrunk__front_trunk_state:
            data = self._controller.command(self._id, 'trunk_open', {'which_trunk': 'front'})
            if data:
                if data['response']['result']:
                    self._FrontTrunk__front_trunk_state = True
            self._FrontTrunk__manual_update_time = time.time()

    def is_locked(self):
        return not self._FrontTrunk__front_trunk_state

    @staticmethod
    def has_battery():
        return False


class RearTrunk(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._RearTrunk__manual_update_time = 0
        self._RearTrunk__rear_trunk_state = False
        self.type = 'rear trunk lock'
        self.hass_type = 'lock'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 13
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_vehicle_params(self._id)
        if data:
            if time.time() - self._RearTrunk__manual_update_time > 60:
                self._RearTrunk__rear_trunk_state = data['rt']

    def open_rear_trunk(self):
        if not self._RearTrunk__rear_trunk_state:
            data = self._controller.command(self._id, 'trunk_open', {'which_trunk': 'rear'})
            if data:
                if data['response']['result']:
                    self._RearTrunk__rear_trunk_state = True
            self._RearTrunk__manual_update_time = time.time()

    def is_locked(self):
        return not self._RearTrunk__rear_trunk_state

    @staticmethod
    def has_battery():
        return False