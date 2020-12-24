# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/internal/timertype.py
# Compiled at: 2018-10-10 01:51:19
# Size of source mod 2**32: 717 bytes
from enum import IntEnum

class TimerType(IntEnum):
    WORKING = (1, )
    BREAK = (2, )
    UNKNOWN = -1