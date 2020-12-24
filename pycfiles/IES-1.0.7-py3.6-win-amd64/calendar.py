# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\calendar.py
# Compiled at: 2018-12-18 03:55:55
# Size of source mod 2**32: 1938 bytes
import pandas as pd

class Calendar(object):

    def __init__(self, var, start_date, end_date):
        self.var = var
        self.cal = self.var.ips_api._framework_getTradeCalendar(start_date, end_date)
        self.cal.date = self.cal.date.apply(lambda x: pd.Timestamp(x))
        self.cal.set_index('date', inplace=True)

    def __getitem__(self, i):
        return self.cal.index[i]

    @property
    def all_sessions(self):
        return self.cal.index

    def slice_locs(self, start_date, end_date):
        return self.cal.index.slice_locs(start_date, end_date)

    def slice(self, start_date, end_date):
        df = self.cal.loc[start_date:end_date]
        return pd.DataFrame({'date':df.index.strftime('%Y%m%d'),  'halfday':df.halfday})

    def append(self, start_date, end_date):
        append_cal = self.var.ips_api._framework_getTradeCalendar(start_date, end_date)
        append_cal.date = append_cal.date.apply(lambda x: pd.Timestamp(x))
        append_cal.set_index('date', inplace=True)
        self.cal = self.cal.append(append_cal)
        self.cal = self.cal[(~self.cal.index.duplicated())]

    def get_first_idx(self, date):
        if self.cal.index[0] >= date:
            return 0
        else:
            if self.cal.index[(-1)] <= date:
                return len(self.cal) - 1
            return len(self.cal.loc[:date]) - 1

    def get_first_ge_idx(self, date):
        if date in self.cal.index:
            return len(self.cal.loc[:date]) - 1
        else:
            if self.cal.index[0] >= date:
                return 0
            if self.cal.index[(-1)] <= date:
                return len(self.cal) - 1
            return len(self.cal.loc[:date])