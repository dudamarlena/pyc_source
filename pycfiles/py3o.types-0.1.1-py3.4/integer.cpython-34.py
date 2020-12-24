# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/types/integer.py
# Compiled at: 2016-05-25 09:34:03
# Size of source mod 2**32: 947 bytes
from py3o.types.types import Py3oTypeMixin

class Py3oInteger(int, Py3oTypeMixin):
    digit_separator = None
    digit_format = 3

    @classmethod
    def get_config_attributes(cls, config):
        res = super(Py3oInteger, cls).get_config_attributes(config)
        if 'digit_separator' in config:
            res['digit_separator'] = config['digit_separator']
        digit_format = config.get('digit_format', None)
        if digit_format is not None:
            res['digit_format'] = int(digit_format)
        return res

    def __str__(self):
        res = super(Py3oInteger, self).__str__()
        if self.digit_separator is not None:
            res = self.digit_separator.join(reversed([res[max(x - self.digit_format, 0):x] for x in range(len(res), 0, -self.digit_format)]))
        return res

    @property
    def odt_value(self):
        return int(self)