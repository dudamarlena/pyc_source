# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/utils/config.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 803 bytes
"""Utilities for the configuration file.
"""

def tobool(value):
    """helper to evaluate a string into a boolean
    WARNING: at the moment value is True by default unless it can
    be evaluated to False matching one of (case insensitive):
        ('false', 'no', 'n', '0')

    :param value: the string to evaluate
    :type value: string

    :returns: True or False depending on the given value
    """
    if value.lower() in ('false', 'no', 'n', '0'):
        value = False
    else:
        value = True
    return value


def bool_setting(config, setting):
    """Read a boolean setting from the configuration file; that setting may be
    expressed as a string.
    """
    value = config.get(setting, True)
    if isinstance(value, str):
        value = tobool(value)
    return value