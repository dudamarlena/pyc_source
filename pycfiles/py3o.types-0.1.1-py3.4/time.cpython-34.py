# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/types/time.py
# Compiled at: 2016-05-25 09:34:03
# Size of source mod 2**32: 857 bytes
import datetime
from py3o.types.types import Py3oTypeMixin

class Py3oTime(datetime.time, Py3oTypeMixin):
    time_format = None

    @classmethod
    def get_config_attributes(cls, config):
        res = super(Py3oTime, cls).get_config_attributes(config)
        if 'time_format' in config:
            res['time_format'] = config['time_format']
        return res

    def __str__(self):
        res = super(Py3oTime, self).__str__()
        if self.time_format:
            res = self.strftime(self.time_format)
        return res

    @property
    def odt_value(self):
        raise NotImplementedError

    @classmethod
    def strptime(cls, date_string, format):
        dt = datetime.datetime.strptime(date_string, format)
        return cls(dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)