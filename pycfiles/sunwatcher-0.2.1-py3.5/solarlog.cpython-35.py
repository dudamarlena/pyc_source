# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sunwatcher/solarlog/solarlog.py
# Compiled at: 2016-08-14 14:12:13
# Size of source mod 2**32: 1926 bytes
from datetime import datetime
from sunwatcher.solarlog.client import Client

class SolarLog(object):

    def __init__(self, solarlog_url):
        self.client = Client(solarlog_url)
        data = self.client.get_data()
        self.time = datetime.strptime(data['time'], '%d.%m.%y %H:%M:%S')
        self.power_ac = data['power_ac']
        self.power_dc = data['power_dc']
        self.voltage_ac = data['voltage_ac']
        self.voltage_dc = data['voltage_dc']
        self.yield_day = data['yield_day']
        self.yield_yesterday = data['yield_yesterday']
        self.yield_month = data['yield_month']
        self.yield_year = data['yield_year']
        self.yield_total = data['yield_total']
        self.consumption_ac = data['consumption_ac']
        self.consumption_day = data['consumption_day']
        self.consumption_yesterday = data['consumption_yesterday']
        self.consumption_month = data['consumption_month']
        self.consumption_year = data['consumption_year']
        self.consumption_total = data['consumption_total']
        self.total_power = data['total_power']

    @property
    def efficiency(self):
        if self.power_dc == 0:
            return 0
        else:
            return self.power_ac / self.power_dc

    @property
    def alternator_loss(self):
        return self.power_dc - self.power_ac

    @property
    def usage(self):
        if self.power_ac == 0:
            return 0
        else:
            return self.consumption_ac / self.power_ac

    @property
    def power_available(self):
        return self.power_ac - self.consumption_ac

    @property
    def capacity(self):
        if self.total_power == 0:
            return 0
        else:
            return self.power_dc / self.total_power