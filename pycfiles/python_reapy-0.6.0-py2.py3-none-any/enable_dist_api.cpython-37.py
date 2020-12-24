# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\reascripts\enable_dist_api.py
# Compiled at: 2019-02-22 02:42:29
# Size of source mod 2**32: 446 bytes
"""
Enable ```reapy`` distant API.

Running this ReaScript from inside REAPER allows to import ``reapy``
from outside. It creates a persistent Web Interface inside REAPER and
adds the ReaScript ``reapy.reascripts.activate_reapy_server`` to the
Actions list. Importing ``reapy`` from outside REAPER will trigger
the latter **via** the Web Interface.
"""
if __name__ == '__main__':
    import reapy
    reapy.config.enable_dist_api()