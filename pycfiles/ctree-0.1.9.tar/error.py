# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/psutil/error.py
# Compiled at: 2013-09-24 00:55:58
__doc__ = "This module is deprecated as exceptions are defined in _error.py\nand are supposed to be accessed from 'psutil' namespace as in:\n- psutil.NoSuchProcess\n- psutil.AccessDenied\n- psutil.TimeoutExpired\n"
import warnings
from psutil._error import *
warnings.warn('psutil.error module is deprecated and scheduled for removal; use psutil namespace instead', category=DeprecationWarning, stacklevel=2)