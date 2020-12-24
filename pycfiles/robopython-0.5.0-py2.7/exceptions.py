# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robopython\pygatt\exceptions.py
# Compiled at: 2020-03-04 11:05:08
"""
Exceptions for pygatt Module.
"""

class BLEError(Exception):
    """Exception class for pygatt."""
    pass


class NotConnectedError(BLEError):
    pass


class NotificationTimeout(BLEError):

    def __init__(self, msg=None, gatttool_output=None):
        super(NotificationTimeout, self).__init__(msg)
        self.gatttool_output = gatttool_output