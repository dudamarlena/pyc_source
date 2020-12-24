# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/holidays/countries/india.py
# Compiled at: 2020-01-26 19:25:31
from datetime import date
from holidays.constants import JAN, MAR, APR, MAY, JUN, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class India(HolidayBase):
    PROVINCES = [
     'AS', 'CG', 'SK', 'KA', 'GJ', 'BR', 'RJ', 'OD',
     'TN', 'AP', 'WB', 'KL', 'HR', 'MH', 'MP', 'UP', 'UK', 'TS']

    def __init__(self, **kwargs):
        self.country = 'IND'
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        self[date(year, JAN, 14)] = 'Makar Sankranti / Pongal'
        if year >= 1950:
            self[date(year, JAN, 26)] = 'Republic Day'
        if year >= 1947:
            self[date(year, AUG, 15)] = 'Independence Day'
        self[date(year, OCT, 2)] = 'Gandhi Jayanti'
        self[date(year, MAY, 1)] = 'Labour Day'
        self[date(year, DEC, 25)] = 'Christmas'
        if self.prov == 'GJ':
            self[date(year, JAN, 14)] = 'Uttarayan'
            self[date(year, MAY, 1)] = 'Gujarat Day'
            self[date(year, OCT, 31)] = 'Sardar Patel Jayanti'
        if self.prov == 'BR':
            self[date(year, MAR, 22)] = 'Bihar Day'
        if self.prov == 'RJ':
            self[date(year, MAR, 30)] = 'Rajasthan Day'
            self[date(year, JUN, 15)] = 'Maharana Pratap Jayanti'
        if self.prov == 'OD':
            self[date(year, APR, 1)] = 'Odisha Day (Utkala Dibasa)'
            self[date(year, APR, 15)] = 'Maha Vishuva Sankranti / Pana Sankranti'
        if self.prov in ('OD', 'AP', 'BR', 'WB', 'KL', 'HR', 'MH', 'UP', 'UK', 'TN'):
            self[date(year, APR, 14)] = "Dr. B. R. Ambedkar's Jayanti"
        if self.prov == 'TN':
            self[date(year, APR, 14)] = 'Puthandu (Tamil New Year)'
            self[date(year, APR, 15)] = 'Puthandu (Tamil New Year)'
        if self.prov == 'WB':
            self[date(year, APR, 14)] = 'Pohela Boishakh'
            self[date(year, APR, 15)] = 'Pohela Boishakh'
            self[date(year, MAY, 9)] = 'Rabindra Jayanti'
        if self.prov == 'AS':
            self[date(year, APR, 15)] = 'Bihu (Assamese New Year)'
        if self.prov == 'MH':
            self[date(year, MAY, 1)] = 'Maharashtra Day'
        if self.prov == 'SK':
            self[date(year, MAY, 16)] = 'Annexation Day'
        if self.prov == 'KA':
            self[date(year, NOV, 1)] = 'Karnataka Rajyotsava'
        if self.prov == 'AP':
            self[date(year, NOV, 1)] = 'Andhra Pradesh Foundation Day'
        if self.prov == 'HR':
            self[date(year, NOV, 1)] = 'Haryana Foundation Day'
        if self.prov == 'MP':
            self[date(year, NOV, 1)] = 'Madhya Pradesh Foundation Day'
        if self.prov == 'KL':
            self[date(year, NOV, 1)] = 'Kerala Foundation Day'
        if self.prov == 'CG':
            self[date(year, NOV, 1)] = 'Chhattisgarh Foundation Day'
        if self.prov == 'TS':
            self[date(year, OCT, 6)] = 'Bathukamma Festival'
            self[date(year, APR, 6)] = 'Eid al-Fitr'


class IN(India):
    pass


class IND(India):
    pass