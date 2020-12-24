# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./file.py
# Compiled at: 2017-08-09 22:30:47
# Size of source mod 2**32: 1176 bytes
import abc, csv

class _VrcgalFile:
    __metaclass__ = abc.ABCMeta

    def __init__(self, file):
        self.load(file)

    @abc.abstractmethod
    def load(self, input):
        """Retrieve data from the input source"""
        pass

    @abc.abstractmethod
    def save(self, output):
        """Save the data object to the output."""
        pass

    def __str__(self):
        headers = ' '.join(self.headers)
        values = ''
        for row in self.data:
            values += '\n'
            values += ' '.join(row.values())

        return '{} \n {}'.format(headers, values)


class XML(_VrcgalFile):

    def load(self, file):
        pass

    def save(self, file):
        pass


class CSV(_VrcgalFile):

    def load(self, file):
        self.data = []
        with open(file, 'r') as (f):
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            for row in reader:
                self.data.append(row)

    def save(self, file):
        pass


class H5(_VrcgalFile):

    def load(self, file):
        pass

    def save(self, file):
        pass


def load(file):
    if '.csv' in file:
        return CSV(file)
    if '.xml' in file:
        return XML(file)
    if '.h5' in file:
        return H5(file)
    raise ValueError('file type not supported')