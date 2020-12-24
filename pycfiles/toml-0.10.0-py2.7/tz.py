# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toml/tz.py
# Compiled at: 2018-10-03 21:56:21
from datetime import tzinfo, timedelta

class TomlTz(tzinfo):

    def __init__(self, toml_offset):
        if toml_offset == 'Z':
            self._raw_offset = '+00:00'
        else:
            self._raw_offset = toml_offset
        self._sign = -1 if self._raw_offset[0] == '-' else 1
        self._hours = int(self._raw_offset[1:3])
        self._minutes = int(self._raw_offset[4:6])

    def tzname(self, dt):
        return 'UTC' + self._raw_offset

    def utcoffset(self, dt):
        return self._sign * timedelta(hours=self._hours, minutes=self._minutes)

    def dst(self, dt):
        return timedelta(0)