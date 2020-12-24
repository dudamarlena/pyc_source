# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/data/value.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1912 bytes
"""This module contains classes and definitions related with *values*.
A value is a metric which will sent to drove
"""
import time
from ..util.network import getfqdn
from . import Data
VALUE_GAUGE = 'g'
VALUE_COUNTER = 'c'
VALUE_TIME = 't'

class Value(Data):
    __doc__ = 'Models a value for drove\n\n    :type nodename: str\n    :param nodename: the node which generate the value\n    :type plugin: str\n    :param plugin: the plugin namespace which generate the value\n    :type value: float or int\n    :param value: the value number to dispatch\n    :type value_type: one of VALUE_COUNTER, VALUE_GAUGE or VALUE_TIME\n    :param value_type: the type of the value\n    :type timestamp: int\n    :param timestamp: the timestamp when the data is created\n    '

    def __init__(self, plugin, value, nodename=None, value_type=VALUE_GAUGE, timestamp=None):
        self.nodename = nodename or getfqdn()
        self.plugin = plugin
        self.value = float(value)
        self.value_id = '%s.%s' % (self.nodename, self.plugin)
        if value_type != VALUE_GAUGE:
            if value_type != VALUE_COUNTER and value_type != VALUE_TIME:
                raise ValueError('Invalid value type')
        self.value_type = value_type
        if timestamp is not None:
            self.timestamp = int(timestamp)
        else:
            self.timestamp = int(time.time())

    def dump(self):
        """Return a dump representation of the value"""
        return 'V|{timestamp}|{nodename}|{plugin}|{value}|{value_type}'.format(timestamp=self.timestamp, nodename=self.nodename, plugin=self.plugin, value=self.value, value_type=self.value_type)

    def __repr__(self):
        return self.dump()