# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/Charger.py
# Compiled at: 2018-06-14 16:08:19
# Size of source mod 2**32: 2843 bytes
from teslajsonpy2.vehicle import VehicleDevice
import time

class ChargerSwitch(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._ChargerSwitch__manual_update_time = 0
        self._ChargerSwitch__charger_state = False
        self.type = 'charger switch'
        self.hass_type = 'switch'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 8
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_charging_params(self._id)
        if data:
            if time.time() - self._ChargerSwitch__manual_update_time > 60:
                if data['charging_state'] != 'Charging':
                    self._ChargerSwitch__charger_state = False
                else:
                    self._ChargerSwitch__charger_state = True

    def start_charge(self):
        if not self._ChargerSwitch__charger_state:
            data = self._controller.command(self._id, 'charge_start')
            if data:
                if data['response']['result']:
                    self._ChargerSwitch__charger_state = True
            self._ChargerSwitch__manual_update_time = time.time()

    def stop_charge(self):
        if self._ChargerSwitch__charger_state:
            data = self._controller.command(self._id, 'charge_stop')
            if data:
                if data['response']['result']:
                    self._ChargerSwitch__charger_state = False
            self._ChargerSwitch__manual_update_time = time.time()

    def is_charging(self):
        return self._ChargerSwitch__charger_state

    @staticmethod
    def has_battery():
        return False


class RangeSwitch(VehicleDevice):

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._RangeSwitch__manual_update_time = 0
        self._RangeSwitch__maxrange_state = False
        self.type = 'maxrange switch'
        self.hass_type = 'switch'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 9
        self.update()

    def update(self):
        self._controller.update(self._id)
        data = self._controller.get_charging_params(self._id)
        if data:
            if time.time() - self._RangeSwitch__manual_update_time > 60:
                self._RangeSwitch__maxrange_state = data['charge_to_max_range']

    def set_max(self):
        if not self._RangeSwitch__maxrange_state:
            data = self._controller.command(self._id, 'charge_max_range')
            if data['response']['result']:
                self._RangeSwitch__maxrange_state = True
            self._RangeSwitch__manual_update_time = time.time()

    def set_standard(self):
        if self._RangeSwitch__maxrange_state:
            data = self._controller.command(self._id, 'charge_standard')
            if data:
                if data['response']['result']:
                    self._RangeSwitch__maxrange_state = False
            self._RangeSwitch__manual_update_time = time.time()

    def is_maxrange(self):
        return self._RangeSwitch__maxrange_state

    @staticmethod
    def has_battery():
        return False