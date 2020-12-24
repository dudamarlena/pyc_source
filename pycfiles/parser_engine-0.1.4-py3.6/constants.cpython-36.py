# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/clue/constants.py
# Compiled at: 2019-03-22 03:43:37
# Size of source mod 2**32: 121 bytes
from enum import IntEnum

class ClueStatus(IntEnum):
    PENDING = 0
    RUNNING = 1
    SUCCESS = 200
    FAILED = 500