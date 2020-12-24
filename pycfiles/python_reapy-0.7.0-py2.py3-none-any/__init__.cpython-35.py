# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/__init__.py
# Compiled at: 2019-02-23 10:11:05
# Size of source mod 2**32: 334 bytes
import sys

def is_inside_reaper():
    """
    Return whether ``reapy`` is imported from inside REAPER.
    """
    inside = hasattr(sys.modules['__main__'], 'obj')
    return inside


from . import config, reascript_api
from .core import *
from .core.reaper import *
from .tools import InsideReaper as inside_reaper