# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/guillem.cabrera/pyvtt/build/lib/pyvtt/vttexc.py
# Compiled at: 2018-03-05 05:30:25
# Size of source mod 2**32: 544 bytes
"""
Exception classes
"""

class Error(Exception):
    __doc__ = "\n    Pyvtt's base exception\n    "


class InvalidTimeString(Error):
    __doc__ = '\n    Raised when parser fail on bad formated time strings\n    '


class InvalidItem(Error):
    __doc__ = '\n    Raised when parser fail to parse a sub title item\n    '


class InvalidIndex(InvalidItem):
    __doc__ = '\n    Raised when parser fail to parse a sub title index\n    '


class InvalidFile(Error):
    __doc__ = '\n    Raised when an invalid file is read or saved\n    '