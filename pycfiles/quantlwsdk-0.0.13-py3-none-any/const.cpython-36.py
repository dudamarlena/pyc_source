# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\const.py
# Compiled at: 2019-11-13 21:25:42
# Size of source mod 2**32: 2222 bytes
from enum import Enum

class CustomEnum(Enum):

    def __repr__(self):
        return '%s.%s' % (
         self.__class__.__name__, self._name_)


class STOP_PROFIT_LOSS_ORDER_STATUS(CustomEnum):
    WAITING_TARGET_ORDER_FILLED = 'WAITING_TARGET_ORDER_FILLED'
    ACTIVE = 'ACTIVE'
    ORDER_SENDED = 'ORDER_SENDED'
    ORDER_CANCELED = 'ORDER_CANCELED'
    TRAILING = 'TRAILING'


class ORDER_TYPE(CustomEnum):
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'


class ORDER_STATUS(CustomEnum):
    PENDING_NEW = 'PENDING_NEW'
    ACTIVE = 'ACTIVE'
    FILLED = 'FILLED'
    REJECTED = 'REJECTED'
    PENDING_CANCEL = 'PENDING_CANCEL'
    CANCELLED = 'CANCELLED'


class POSITION_SIDE(CustomEnum):
    UN_KNOWN = 'UN_KNOWN'
    LONG = 'LONG'
    SHORT = 'SHORT'