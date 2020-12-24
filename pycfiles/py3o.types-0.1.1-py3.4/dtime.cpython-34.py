# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/types/dtime.py
# Compiled at: 2016-05-25 09:34:03
# Size of source mod 2**32: 1046 bytes
from datetime import datetime
from py3o.types.types import Py3oTypeMixin

class Py3oDatetime(datetime, Py3oTypeMixin):
    datetime_format = None

    @classmethod
    def get_config_attributes(cls, config):
        res = super(Py3oDatetime, cls).get_config_attributes(config)
        if 'datetime_format' in config:
            res['datetime_format'] = config['datetime_format']
        elif 'date_format' in config:
            if 'time_format' in config:
                res['datetime_format'] = '{date} {time}'.format(date=config['date_format'], time=config['time_format'])
        return res

    def __str__(self):
        res = super(Py3oDatetime, self).__str__()
        if self.datetime_format:
            res = self.strftime(self.datetime_format)
        return res

    @property
    def odt_value(self):
        raise NotImplementedError

    @classmethod
    def strptime(cls, date_string, format):
        return super(Py3oDatetime, cls).strptime(date_string, format)