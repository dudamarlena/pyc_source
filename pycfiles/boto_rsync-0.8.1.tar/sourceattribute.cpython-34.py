# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudsearch/sourceattribute.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3156 bytes


class SourceAttribute(object):
    """SourceAttribute"""
    ValidDataFunctions = ('Copy', 'TrimTitle', 'Map')

    def __init__(self):
        self.data_copy = {}
        self._data_function = self.ValidDataFunctions[0]
        self.data_map = {}
        self.data_trim_title = {}

    @property
    def data_function(self):
        return self._data_function

    @data_function.setter
    def data_function(self, value):
        if value not in self.ValidDataFunctions:
            valid = '|'.join(self.ValidDataFunctions)
            raise ValueError('data_function must be one of: %s' % valid)
        self._data_function = value