# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyzenobase/zenobase_event.py
# Compiled at: 2015-09-24 11:31:04
# Size of source mod 2**32: 2121 bytes
from datetime import datetime
from pyzenobase import fmt_datetime
_VALID_FIELDS = ['bits', 'concentration', 'count', 'currency', 'distance',
 'distance/volume', 'duration', 'energy', 'frequency', 'height',
 'humidity', 'location', 'moon', 'note', 'pace', 'percentage',
 'pressure', 'rating', 'resource', 'sound', 'source', 'tag',
 'temperature', 'timestamp', 'velocity', 'volume', 'weight']

class ZenobaseEvent(dict):
    __doc__ = '\n        Provides simple structure checking\n    '

    def __init__(self, data):
        super(ZenobaseEvent, self).__init__(self)
        for field in data:
            assert field in _VALID_FIELDS
            self[field] = data[field]

        self.clean_data()

    def clean_data(self):
        """Ensures data is Zenobase compatible and patches it if possible,
        if cleaning is not possible it'll raise an appropriate exception"""
        if 'timestamp' in self:
            self._check_timestamp()
            if type(self['timestamp']) == list:

                def datetime_to_string(dt):
                    if type(dt) == datetime:
                        return fmt_datetime(dt)
                    return dt

                self['timestamp'] = list(map(datetime_to_string, self['timestamp']))
        else:
            if type(self['timestamp']) == datetime:
                self['timestamp'] = fmt_datetime(self['timestamp'])
            if 'volume' in self:
                self['volume']['unit'] = self['volume']['unit'].replace('l', 'L')
            if 'weight' in self:
                if self['weight']['unit'] in ('mcg', 'µg'):
                    self['weight']['unit'] = 'ug'

    def _check_timestamp(self):
        if type(self['timestamp']) not in (str, datetime, list):
            if type(self['timestamp']) != list or all(map(lambda x: type(x) in (str, datetime), self['timestamp'])):
                raise TypeError('timestamp must be string, datetime or list of strings/datetimes')