# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/time.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 786 bytes
"""
This module contains the main classes for handling requests to the AppDynamics REST API.
"""
from __future__ import absolute_import
from datetime import datetime
from time import mktime

def from_ts(ms):
    """
    Converts a timestamp from AppDynamics internal format to a Python :class:`datetime <datetime.datetime>` object.

    :param long ms: Timestamp expressed as milliseconds since epoch.
    :returns: Converted value.
    :rtype: datetime
    """
    return datetime.fromtimestamp(ms / 1000)


def to_ts(dt):
    """
    Converts a timestamp from Python :class:`datetime <datetime.datetime>` to AppDynamics format.

    :param datetime dt: Timestamp to convert.
    :returns: Converted value.
    :rtype: long
    """
    return int(mktime(dt.timetuple())) * 1000