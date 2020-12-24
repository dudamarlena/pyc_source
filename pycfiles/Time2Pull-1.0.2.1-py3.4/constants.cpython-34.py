# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/time2pull/constants.py
# Compiled at: 2014-06-16 15:45:18
# Size of source mod 2**32: 262 bytes
"""
Contains the application constans and enumerations
"""
from enum import IntEnum

class RemoteStatus(IntEnum):
    up_to_date = 0
    behind = 1
    ahead = 2
    diverged = 3


class TrayIconType(IntEnum):
    light = 0
    dark = 1