# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\python\EasyVision\EasyVision\vision\exceptions.py
# Compiled at: 2019-02-06 10:22:12
"""Exceptions used for Vision capturing adapters.

"""
from EasyVision.exceptions import EasyVisionError

class DeviceNotFound(EasyVisionError):
    pass