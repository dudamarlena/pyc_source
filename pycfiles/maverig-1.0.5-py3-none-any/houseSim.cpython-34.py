# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\utils\houseSim.py
# Compiled at: 2014-10-21 14:50:33
# Size of source mod 2**32: 2319 bytes
import arrow, mosaik_api
from mosaik_csv import CSV
DATE_FORMAT = 'YYYY-MM-DD HH:mm:ss'
meta = {'models': {'House': {'public': True, 
                      'params': [],  'attrs': [
                                'P',
                                'num_hh',
                                'num_res']}}}

class HouseSim(CSV):

    def __init__(self):
        super(CSV, self).__init__(meta)
        self.start_date = None
        self.datafile = None
        self.next_row = None
        self.modelname = None
        self.attrs = None
        self.eids = []
        self.cache = None
        self.next_date = None
        self.num_hh = None
        self.num_res = None

    def init(self, sid, sim_start, datafile):
        """ overrides CSV init with retrieving static data (num_hh and num_res) in line 2 and 3 of csv file """
        self.start_date = arrow.get(sim_start, DATE_FORMAT)
        self.next_date = self.start_date
        self.datafile = open(datafile)
        self.modelname = next(self.datafile).strip()
        self.num_hh = next(self.datafile).split(',')[1].strip()
        self.num_res = next(self.datafile).split(',')[1].strip()
        next(self.datafile)
        self.attrs = meta['models']['House']['attrs']
        self._read_next_row()
        if self.start_date < self.next_row[0]:
            raise ValueError('Start date "%s" not in CSV file.' % self.start_date.format(DATE_FORMAT))
        while self.start_date > self.next_row[0]:
            self._read_next_row()
            if self.next_row is None:
                raise ValueError('Start date "%s" not in CSV file.' % self.start_date.format(DATE_FORMAT))
                continue

        return self.meta

    def get_data(self, outputs):
        self.cache['num_hh'] = self.num_hh
        self.cache['num_res'] = self.num_res
        return super().get_data(outputs)


def main():
    return mosaik_api.start_simulation(HouseSim(), 'maverig house simulator')