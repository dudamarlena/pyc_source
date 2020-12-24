# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weresync/exception.py
# Compiled at: 2019-06-14 22:29:48
# Size of source mod 2**32: 1553 bytes
"""Exceptions used by WereSync"""

class DeviceError(Exception):
    __doc__ = 'Exception thrown to show errors caused by an issue with a specific\n    device.'

    def __init__(self, device, message, errors=None):
        self.device = device
        self.message = message
        self.errors = errors


class CopyError(Exception):
    __doc__ = 'Exception thrown to show errors caused by an issue copying data,\n    usually both devices face the issue.'

    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors


class UnsupportedDeviceError(Exception):
    __doc__ = 'Exception thrown to show that action is not supported on the partition\n    table type of the device.'


class InvalidVersionError(Exception):
    __doc__ = 'Exception thrown when the version of python being used does not support\n    the feature.'


class PluginNotFoundError(Exception):
    __doc__ = 'Exception thrown when the passed plugin is not found.'