# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/types/types/float.py
# Compiled at: 2016-05-25 09:34:03
# Size of source mod 2**32: 1183 bytes
from py3o.types.types import Py3oTypeMixin

class Py3oFloat(float, Py3oTypeMixin):
    digit_separator = None
    digit_format = 3
    decimal_separator = '.'

    @classmethod
    def get_config_attributes(cls, config):
        res = super(Py3oFloat, cls).get_config_attributes(config)
        if 'digit_separator' in config:
            res['digit_separator'] = config['digit_separator']
        digit_format = config.get('digit_format', None)
        if digit_format is not None:
            res['digit_format'] = int(digit_format)
        if 'decimal_separator' in config:
            res['decimal_separator'] = config['decimal_separator']
        return res

    def __str__(self):
        res = super(Py3oFloat, self).__str__()
        integer, decimal = res.split('.')
        if self.digit_separator is not None:
            integer = self.digit_separator.join(reversed([integer[max(x - self.digit_format, 0):x] for x in range(len(integer), 0, -self.digit_format)]))
        return self.decimal_separator.join((integer, decimal))

    @property
    def odt_value(self):
        return float(self)