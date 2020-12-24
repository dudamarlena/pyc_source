# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intercept/data_format.py
# Compiled at: 2018-12-27 16:24:21
# Size of source mod 2**32: 118 bytes
from enum import Enum, auto

class DataFormat(Enum):
    CLEAN = auto()
    ANSI = auto()
    KEEP = auto()