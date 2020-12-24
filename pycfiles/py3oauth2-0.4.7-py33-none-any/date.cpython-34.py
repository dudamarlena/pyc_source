# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/types/date.py
# Compiled at: 2016-05-25 09:34:03
# Size of source mod 2**32: 812 bytes
import datetime
from py3o.types.types import Py3oTypeMixin

class Py3oDate(datetime.date, Py3oTypeMixin):
    date_format = None

    @classmethod
    def get_config_attributes(cls, config):
        res = super(Py3oDate, cls).get_config_attributes(config)
        if 'date_format' in config:
            res['date_format'] = config['date_format']
        return res

    def __str__(self):
        res = super(Py3oDate, self).__str__()
        if self.date_format:
            res = self.strftime(self.date_format)
        return res

    def odt_value(self):
        raise NotImplementedError

    @classmethod
    def strptime(cls, date_string, format):
        dt = datetime.datetime.strptime(date_string, format)
        return cls(dt.year, dt.month, dt.day)