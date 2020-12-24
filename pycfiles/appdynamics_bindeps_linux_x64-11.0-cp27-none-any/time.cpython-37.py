# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/time.py
# Compiled at: 2020-03-11 17:47:43
# Size of source mod 2**32: 786 bytes
__doc__ = '\nThis module contains the main classes for handling requests to the AppDynamics REST API.\n'
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