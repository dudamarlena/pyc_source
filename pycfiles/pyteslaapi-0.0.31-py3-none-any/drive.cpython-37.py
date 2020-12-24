# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tamell/code/pyteslaapi/pyteslaapi/drive.py
# Compiled at: 2018-11-02 18:40:44
# Size of source mod 2**32: 785 bytes


class Drive:

    def __init__(self, vehicle):
        self.vehicle = vehicle

    @property
    def attributes(self):
        return self.vehicle._drive_data

    @property
    def shift_state(self):
        if not self.vehicle._drive_data['shift_state']:
            return 'P'
        return self.vehicle._drive_data['shift_state']

    @property
    def speed(self):
        return self.vehicle._drive_data['speed']

    @property
    def latitude(self):
        return self.vehicle._drive_data['latitude']

    @property
    def longitude(self):
        return self.vehicle._drive_data['longitude']

    @property
    def heading(self):
        return self.vehicle._drive_data['heading']

    @property
    def gps_as_of(self):
        return self.vehicle._drive_data['gps_as_of']