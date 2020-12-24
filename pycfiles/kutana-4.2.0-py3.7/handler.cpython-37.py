# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kutana/handler.py
# Compiled at: 2020-05-02 08:54:53
# Size of source mod 2**32: 215 bytes
from collections import namedtuple
from enum import Enum

class HandlerResponse(Enum):
    COMPLETE = 1
    SKIPPED = 2


Handler = namedtuple('Handler', [
 'handle', 'group_state', 'user_state', 'priority'])