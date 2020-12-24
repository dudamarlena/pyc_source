# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/vehicle.py
# Compiled at: 2018-02-18 18:17:49
# Size of source mod 2**32: 477 bytes


class VehicleDevice:

    def __init__(self, data, controller):
        self._id = data['id']
        self._vin = data['vin']
        self._raw_name = data['name']
        self._short_name = ' '.join(self._raw_name.split()[:3])
        self._controller = controller
        self.should_poll = True

    def _name(self):
        return '{} {}'.format(self._short_name, self.type)

    def _uniq_name(self):
        return '{} {} {}'.format(self._short_name, self._id, self.type)