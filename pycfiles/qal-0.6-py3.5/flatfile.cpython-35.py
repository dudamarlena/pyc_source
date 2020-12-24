# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/dataset/flatfile.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 7010 bytes
"""
Created on Sep 14, 2012

@author: Nicklas Boerjesson
"""
from datetime import date
import datetime
from itertools import islice
import csv
from urllib.parse import unquote
from qal.common.meta import readattr
from qal.common.strings import make_path_absolute, string_to_bool
from qal.dataset.custom import CustomDataset

class FlatfileDataset(CustomDataset):
    __doc__ = 'This class loads a flat file into an array, self.data_table.'
    delimiter = None
    has_header = None
    filename = None
    field_names = None
    csv_dialect = None
    quoting = None
    quotechar = '"'
    escapechar = None
    lineterminator = None
    skipinitialspace = None

    def __init__(self, _delimiter=None, _filename=None, _has_header=None, _csv_dialect=None, _resource=None, _quoting=None, _quotechar=None, _skipinitialspace=None):
        """Constructor"""
        super(FlatfileDataset, self).__init__()
        if _resource is not None:
            self.read_resource_settings(_resource)
        else:
            self.delimiter = _delimiter
            self.filename = _filename
            self.has_header = _has_header
            self.csv_dialect = _csv_dialect
            self.quoting = _quoting
            self.quotechar = _quotechar
            self.skipinitialspace = _skipinitialspace

    def read_resource_settings(self, _resource):
        if _resource.type.upper() != 'FLATFILE':
            raise Exception('FlatfileDataset.read_resource_settings.parse_resource error: Wrong resource type: ' + _resource.type)
        self._base_path = _resource.base_path
        self.filename = readattr(_resource, 'filename')
        self.delimiter = readattr(_resource, 'delimiter')
        self.csv_dialect = readattr(_resource, 'csv_dialect')
        self.quoting = readattr(_resource, 'quoting')
        self.escapechar = readattr(_resource, 'escapechar')
        self.quotechar = readattr(_resource, 'quotechar', '"')
        self.skipinitialspace = readattr(_resource, 'skipinitialspace')
        if hasattr(_resource, 'lineterminator'):
            self.lineterminator = bytes(_resource.lineterminator, 'UTF-8').decode('unicode-escape')
        if readattr(_resource, 'has_header'):
            self.has_header = string_to_bool(str(_resource.has_header))
        else:
            self.has_header = None

    def write_resource_settings(self, _resource):
        _resource.type = _resource.type
        _resource.filename = self.filename
        _resource.delimiter = self.delimiter
        _resource.has_header = self.has_header
        _resource.csv_dialect = self.csv_dialect
        _resource.quoting = self.quoting
        if self.escapechar:
            _resource.escapechar = self.escapechar
        _resource.lineterminator = self.lineterminator
        _resource.quotechar = self.quotechar
        _resource.skipinitialspace = self.skipinitialspace

    @staticmethod
    def _quotestr_to_constants(_str):
        if _str is None:
            return csv.QUOTE_NONE
        if _str.upper() == 'MINIMAL':
            return csv.QUOTE_MINIMAL
        if _str.upper() == 'ALL':
            return csv.QUOTE_ALL
        if _str.upper() == 'NONNUMERIC':
            return csv.QUOTE_NONNUMERIC
        raise Exception('Error in _quotestr_to_constants: ' + str(_str) + ' is an invalid quotestr.')

    def load(self):
        """Load data"""
        print("FlatfileDataset.load: Filename='" + str(self.filename) + "', Delimiter='" + str(self.delimiter) + "'" + ', Base_path ' + str(self._base_path))
        _file = open(make_path_absolute(self.filename, self._base_path), 'r')
        _reader = csv.reader(_file, delimiter=self.delimiter, quoting=self._quotestr_to_constants(self.quoting), quotechar=self.quotechar, skipinitialspace=self.skipinitialspace)
        _first_row = True
        self.data_table = []
        for _row in _reader:
            if _first_row:
                if self.has_header:
                    self.field_names = [_curr_col.replace("'", '').replace('"', '') for _curr_col in _row]
                    print('self.field_names :' + str(self.field_names))
                else:
                    self.field_names = []
                    for _curr_idx in range(0, len(_row)):
                        self.field_names.append('Field_' + str(_curr_idx))

                _first_row = False
            else:
                self.data_table.append(_row)

        _file.close()
        return self.data_table

    def save(self, _save_as=None):
        """Save data"""
        print("FlatfileDataset.save: Filename='" + str(self.filename) + "', Delimiter='" + str(self.delimiter) + "'")
        if _save_as:
            _filename = _save_as
        else:
            _filename = make_path_absolute(self.filename, self._base_path)
        _file = open(_filename, 'w')
        if self.lineterminator:
            _writer = csv.writer(_file, delimiter=self.delimiter, quoting=self._quotestr_to_constants(self.quoting), quotechar=self.quotechar, skipinitialspace=self.skipinitialspace, lineterminator=self.lineterminator)
        else:
            _writer = csv.writer(_file, delimiter=self.delimiter, quoting=self._quotestr_to_constants(self.quoting), quotechar=self.quotechar, skipinitialspace=self.skipinitialspace)
        if self.has_header:
            _writer.writerow(self.field_names)
        _writer.writerows(self.data_table)
        _file.close()