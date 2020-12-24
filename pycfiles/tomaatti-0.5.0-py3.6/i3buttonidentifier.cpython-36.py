# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/internal/i3buttonidentifier.py
# Compiled at: 2018-06-19 09:05:36
# Size of source mod 2**32: 801 bytes
from enum import Enum

class I3ButtonIdentifier(Enum):
    LEFT_MOUSE_BUTTON = (1, )
    MIDDLE_MOUSE_BUTTON = (2, )
    RIGHT_MOUSE_BUTTON = (3, )
    MOUSE_SCROLL_UP = (4, )
    MOUSE_SCROLL_DOWN = (5, )