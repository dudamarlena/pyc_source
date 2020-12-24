# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/psutil/error.py
# Compiled at: 2013-09-24 00:55:58
"""This module is deprecated as exceptions are defined in _error.py
and are supposed to be accessed from 'psutil' namespace as in:
- psutil.NoSuchProcess
- psutil.AccessDenied
- psutil.TimeoutExpired
"""
import warnings
from psutil._error import *
warnings.warn('psutil.error module is deprecated and scheduled for removal; use psutil namespace instead', category=DeprecationWarning, stacklevel=2)