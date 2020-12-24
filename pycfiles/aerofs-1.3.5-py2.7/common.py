# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/aerofs/sdk/common.py
# Compiled at: 2016-01-14 18:25:50
import enum

class ContentState(enum.Enum):
    AVAILABLE = 'AVAILABLE'
    SYNCING = 'SYNCING'
    DESELECTED = 'DESELECTED'
    INSUFFICIENT_STORAGE = 'INSUFFICIENT_STORAGE'
    UNKNOWN = 'UNKNOWN'


class Permission(enum.Enum):
    WRITE = 'WRITE'
    MANAGE = 'MANAGE'