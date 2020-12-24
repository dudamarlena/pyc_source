# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\reconnect.py
# Compiled at: 2019-10-27 04:01:10
# Size of source mod 2**32: 573 bytes
import importlib, reapy
from reapy.errors import DisabledDistAPIError
from . import _inside_reaper

def reconnect():
    if not reapy.is_inside_reaper():
        try:
            _inside_reaper._WEB_INTERFACE = _inside_reaper.WebInterface(reapy.config.WEB_INTERFACE_PORT)
            _inside_reaper._CLIENT = _inside_reaper.Client(_inside_reaper._WEB_INTERFACE.get_reapy_server_port())
        except DisabledDistAPIError:
            pass

        importlib.reload(reapy.reascript_api)