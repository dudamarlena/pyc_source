# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cachet_url_monitor/latency_unit.py
# Compiled at: 2020-01-28 04:43:05
# Size of source mod 2**32: 724 bytes
from typing import Dict
seconds_per_unit = {'ms':1000,  'milliseconds':1000,  's':1,  'seconds':1,  'm':float(1) / 60,  'minutes':float(1) / 60, 
 'h':float(1) / 3600,  'hours':float(1) / 3600}
seconds_per_unit: Dict[(str, float)]

def convert_to_unit(time_unit: str, value: float):
    """
    Will convert the given value from seconds to the given time_unit.

    :param time_unit: The time unit to which the value will be converted to, from seconds.
    This is a string parameter. The unit must be in the short form.
    :param value: The given value that will be converted. This value must be in seconds.
    :return: The converted value.
    """
    return value * seconds_per_unit[time_unit]