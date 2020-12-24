# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benlong/Developer/git/vrcgal_py/vrcgal_py/data_file.py
# Compiled at: 2017-08-15 08:01:13
# Size of source mod 2**32: 2280 bytes
import abc, csv, h5py
from .data_column import DataColumn

class _DataFile:
    __metaclass__ = abc.ABCMeta

    def __init__(self, file, header_row=0):
        self._columns = []
        self._headers = []
        self.load(file, header_row)

    @abc.abstractmethod
    def load(self, input):
        """Retrieve data from the input source"""
        pass

    @property
    def columns(self):
        return self._columns

    @property
    def headers(self):
        return self._headers

    def get(self, header):
        if header not in self.headers:
            raise ValueError('missing column')
        return self.columns[self.headers.index(header)]


class CSV(_DataFile):

    def load(self, file, header_row):
        self._columns = []
        self._headers = []
        with open(file, 'r') as (f):
            reader = list(csv.reader(f))
            columns = range(0, len(reader[header_row]))
            for column in columns:
                column_data = []
                for row in reader:
                    try:
                        column_data.append(float(row[column]))
                    except ValueError:
                        column_data.append(row[column])

                self._headers.append(column_data[header_row])
                self._columns.append(DataColumn(column_data[header_row], column_data[header_row + 1:]))


class H5(_DataFile):

    def load(self, file, header_row):
        f = h5py.File(file, 'r')
        self._heaers = []
        self._columns = []
        self._parse(f)

    def _parse(self, data, header=''):
        for k, v in data.items():
            column = '{}/{}'.format(header, k)
            if not hasattr(v, 'items'):
                self._headers.append(column)
                self._columns.append(DataColumn(column, v[:]))
            else:
                self._parse(v, column)


def load(file, header_row=0):
    if '.csv' in file:
        return CSV(file, header_row)
    if '.h5' in file:
        return H5(file, header_row)
    raise ValueError('file type not supported')