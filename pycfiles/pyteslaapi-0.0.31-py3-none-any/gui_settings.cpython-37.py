# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tamell/code/pyteslaapi/pyteslaapi/gui_settings.py
# Compiled at: 2018-11-02 18:42:27
# Size of source mod 2**32: 752 bytes


class GuiSettings:

    def __init__(self, vehicle):
        self.vehicle = vehicle

    @property
    def attributes(self):
        return self.vehicle._gui_settings_data

    @property
    def distance_units(self):
        return self.vehicle._gui_settings_data['gui_distance_units']

    @property
    def temperature_units(self):
        return self.vehicle._gui_settings_data['gui_temperature_units']

    @property
    def charge_rate_units(self):
        return self.vehicle._gui_settings_data['gui_charge_rate_units']

    @property
    def gui_24_hour_time(self):
        return self.vehicle._gui_settings_data['gui_24_hour_time']

    @property
    def range_display(self):
        return self.vehicle._gui_settings_data['gui_range_display']