# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider_common/notify/constants/signals.py
# Compiled at: 2019-04-16 05:50:15
# Size of source mod 2**32: 620 bytes
from enum import IntEnum

class SignalEnum(IntEnum):
    ENGINE_STARTED = 1
    ENGINE_STOPPED = 2
    SPIDER_OPENED = 3
    SPIDER_IDLE = 4
    SPIDER_CLOSED = 5
    SPIDER_ERROR = 6
    REQUEST_SCHEDULED = 7
    REQUEST_DROPPED = 8
    REQUEST_REACHED_DOWNLOADER = 9
    RESPONSE_RECEIVED = 10
    RESPONSE_DOWNLOADED = 11
    ITEM_SCRAPED = 12
    ITEM_DROPPED = 13
    ITEM_ERROR = 14
    STATS_SPIDER_OPENED = SPIDER_OPENED
    STATS_SPIDER_CLOSING = SPIDER_CLOSED
    STATS_SPIDER_CLOSED = SPIDER_CLOSED
    ITEM_PASSED = ITEM_SCRAPED
    REQUEST_RECEIVED = REQUEST_SCHEDULED