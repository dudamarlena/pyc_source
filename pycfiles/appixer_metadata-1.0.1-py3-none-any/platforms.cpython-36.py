# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/automation/mobile/platforms.py
# Compiled at: 2017-04-05 02:21:12
# Size of source mod 2**32: 657 bytes
from enum import Enum

class Platform(Enum):
    UNKNOWN = 0
    IOS = 1
    ANDROID = 2