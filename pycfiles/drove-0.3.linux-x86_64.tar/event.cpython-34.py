# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/data/event.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1886 bytes
"""This module contains classes and definitions related with *events*.
An event is a notification emitted by some plugin to warn about any
condition.
"""
import time
from ..util.network import getfqdn
from . import Data

class Severity(object):
    __doc__ = 'Model the severity of an event.\n\n    >>> Severity.OKAY == 0\n    >>> Severity.WARNING == 1\n    >>> Severity.CRITICAL == 2\n    >>> Severity.MISSING == 3\n    '
    OKAY = 0
    WARNING = 1
    CRITICAL = 2
    MISSING = 3


class Event(Data):
    __doc__ = 'Models an event for drove\n\n    :type nodename: str\n    :param nodename: the node which generate the value\n    :type plugin: str\n    :param plugin: the plugin namespace which generate the value\n    :type value: float or int\n    :param value: the value number to dispatch\n    :type value_type: one of VALUE_COUNTER, VALUE_GAUGE or VALUE_TIME\n    :param value_type: the type of the value\n    :type timestamp: int\n    :param timestamp: the timestamp when the data is created\n    '

    def __init__(self, plugin, severity, message, nodename=None, timestamp=None):
        self.nodename = nodename or getfqdn()
        self.plugin = plugin
        self.message = message
        self.severity = severity
        if timestamp is not None:
            self.timestamp = int(timestamp)
        else:
            self.timestamp = int(time.time())

    def dump(self):
        """Return a dump representation of the event"""
        return 'E|{timestamp}|{nodename}|{plugin}|{severity}|{message}'.format(timestamp=self.timestamp, nodename=self.nodename, plugin=self.plugin, severity=self.severity, message=self.message)

    def __repr__(self):
        return self.dump()