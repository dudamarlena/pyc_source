# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benlong/Developer/git/vrcgal_py/vrcgal_py/file.py
# Compiled at: 2017-08-12 10:24:54
# Size of source mod 2**32: 1638 bytes
import abc, csv, h5py

class _VrcgalFile:
    __metaclass__ = abc.ABCMeta

    def __init__(self, file, header_row=0):
        self.header_row = header_row
        self.load(file)

    @abc.abstractmethod
    def load(self, input):
        """Retrieve data from the input source"""
        pass

    @abc.abstractmethod
    def save(self, output):
        """Save the data object to the output."""
        pass


class XML(_VrcgalFile):

    def load(self, file):
        pass

    def save(self, file):
        pass


class CSV(_VrcgalFile):

    def load(self, file):
        self.data = []
        with open(file, 'r') as (f):
            reader = csv.reader(f)
            [self.data.append(row) for row in reader]
            self.headers = self.data[self.header_row]

    def save(self, file):
        pass

    def get(self, column):
        data = []
        index = self.headers.index(column)
        [data.append(row[index]) for row in self.data]
        data.pop(0)
        return DataColumn(column, data)


class H5(_VrcgalFile):

    def load(self, file):
        self.data = h5py.File(file, 'r')
        self.headers = []

    def save(self, file):
        pass


class DataColumn:

    def __init__(self, column, data):
        self.column = column.replace(' ', '')
        self.data = [float(row.replace(' ', '')) for row in data if row != column]

    def __repr__(self):
        out = self.column
        out += ':\n\n'
        for dat in self.data:
            out += '\n{}'.format(dat)

        return out


def load(file, header_row=0):
    if '.csv' in file:
        return CSV(file, header_row)
    else:
        if '.xml' in file:
            return XML(file, header_row)
        if '.h5' in file:
            return H5(file, header_row)
    raise ValueError('file type not supported')