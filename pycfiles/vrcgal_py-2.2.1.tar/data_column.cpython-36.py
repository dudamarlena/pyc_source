# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benlong/Developer/git/vrcgal_py/vrcgal_py/data_column.py
# Compiled at: 2017-08-14 20:58:00
# Size of source mod 2**32: 389 bytes


class DataColumn:

    def __init__(self, header, data):
        self._header = header
        self._data = data

    @property
    def header(self):
        return self._header

    @property
    def data(self):
        return self._data

    def __len__(self):
        return len(self.data)