# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\reascripts\disable_dist_api.py
# Compiled at: 2019-02-22 02:44:15
# Size of source mod 2**32: 405 bytes
"""
Disable ```reapy`` distant API.

Running this ReaScript from inside REAPER disables ``reapy`` imports
from outside. It deletes the persistent Web Interface and removes the
ReaScript ``reapy.reascripts.activate_reapy_server`` from the Actions
list.

See also
--------
reapy.reascripts.enable_dist_api
"""
if __name__ == '__main__':
    import reapy
    reapy.config.disable_dist_api()