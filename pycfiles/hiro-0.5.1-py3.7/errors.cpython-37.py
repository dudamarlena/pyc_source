# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/hiro/errors.py
# Compiled at: 2019-10-04 00:47:03
# Size of source mod 2**32: 894 bytes
"""
exceptions used by hiro.
"""

class SegmentNotComplete(Exception):
    __doc__ = "\n    used to raise an exception if an async segment hasn't completed yet\n    "


class TimeOutofBounds(AttributeError):
    __doc__ = '\n    used to raise an exception when time is rewound beyond the epoch\n    '

    def __init__(self, oob_time):
        message = "you've frozen time at a point before the epoch (%d).hiro only supports going back to 1970/01/01 07:30:00" % oob_time
        super(TimeOutofBounds, self).__init__(message)


class InvalidTypeError(TypeError):
    __doc__ = '\n    used to raise an exception when an invalid type is provided\n    for type operations\n    '

    def __init__(self, value):
        message = '%s provided when only float, int, datetime, or date objectsare supported' % type(value)
        super(InvalidTypeError, self).__init__(message)