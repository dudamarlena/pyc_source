# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\__init__.py
# Compiled at: 2020-05-09 09:41:03
# Size of source mod 2**32: 881 bytes
import sys

def is_inside_reaper():
    """
    Return whether ``reapy`` is imported from inside REAPER.

    If ``reapy`` is run from inside a REAPER instance but currently
    controls another REAPER instance on a slave machine (with
    ``reapy.machines.select_machine``), return False.
    """
    inside = hasattr(sys.modules['__main__'], 'obj')
    if not inside:
        return False
    try:
        return machines.get_selected_machine_host() is None
    except NameError:
        return True


from .tools import connect, connect_to_default_machine, dist_api_is_enabled, inside_reaper, reconnect
from . import reascript_api
from .core import *
from .core.reaper import *
__version__ = '0.7.0'