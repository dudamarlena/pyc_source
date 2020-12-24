# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/primitive.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 516 bytes
from typing import NewType
UserID = NewType('UserID', str)
EventID = NewType('EventID', str)
RoomID = NewType('RoomID', str)
RoomAlias = NewType('RoomAlias', str)
FilterID = NewType('FilterID', str)
ContentURI = NewType('ContentURI', str)
SyncToken = NewType('SyncToken', str)