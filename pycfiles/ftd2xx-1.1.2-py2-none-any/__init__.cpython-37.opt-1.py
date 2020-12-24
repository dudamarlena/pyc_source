# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ftd2xx\__init__.py
# Compiled at: 2019-09-26 14:10:14
# Size of source mod 2**32: 565 bytes
"""
Control FTDI USB chips.

Open a handle using ftd2xx.open or ftd2xx.openEx and use the methods
on the object thus returned.

There are a few convenience functions too
"""
from __future__ import absolute_import
import sys
from .ftd2xx import *
__all__ = [
 'call_ft', 'listDevices', 'getLibraryVersion',
 'createDeviceInfoList', 'getDeviceInfoDetail', 'open',
 'openEx', 'FTD2XX',
 'DeviceError', 'ft_program_data']
if sys.platform == 'win32':
    __all__ += ['w32CreateFile']
else:
    __all__ += ['getVIDPID', 'setVIDPID']