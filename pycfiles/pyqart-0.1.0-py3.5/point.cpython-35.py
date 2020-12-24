# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/painter/point.py
# Compiled at: 2016-07-31 11:56:50
# Size of source mod 2**32: 822 bytes
from enum import Enum, unique
__all__ = [
 'QrPointType', 'QrPoint']

@unique
class QrPointType(Enum):
    UNKNOWN = 0
    POSITION = 1
    ALIGNMENT = 2
    TIMING = 3
    FORMAT = 4
    VERSION_PATTERN = 5
    UNUSED = 6
    DATA = 7
    CORRECTION = 8
    EXTRA = 9


class QrPoint(object):

    def __init__(self, fill, type_=QrPointType.UNKNOWN, offset=-1, invert=False):
        self.fill = fill
        self.type = type_
        self.offset = offset
        self.invert = invert