# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/automation/mobile/platforms.py
# Compiled at: 2017-04-05 02:21:12
# Size of source mod 2**32: 657 bytes
from enum import Enum

class Platform(Enum):
    UNKNOWN = 0
    IOS = 1
    ANDROID = 2