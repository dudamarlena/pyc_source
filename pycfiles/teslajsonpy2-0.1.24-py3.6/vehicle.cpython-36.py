# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/vehicle.py
# Compiled at: 2018-06-14 15:51:08
# Size of source mod 2**32: 699 bytes


class VehicleDevice:

    def __init__(self, data, controller):
        self._id = data['id']
        self._vehicle_id = data['vehicle_id']
        self._vin = data['vin']
        self._state = data['state']
        self._controller = controller
        self.should_poll = True

    def _name(self):
        return 'Tesla Model {} {}'.format(str(self._vin[3]).upper(), self.type)

    def _uniq_name(self):
        return 'Tesla Model {} {} {}'.format(str(self._vin[3]).upper(), self._vin, self.type)

    def id(self):
        return self._id

    @staticmethod
    def is_armable():
        return False

    @staticmethod
    def is_armed():
        return False