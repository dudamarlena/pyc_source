# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/event/ephemeral.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1514 bytes
from typing import List, Dict
from attr import dataclass
from ..util import SerializableAttrs, SerializableEnum
from ..primitive import UserID, RoomID, EventID
from .base import BaseEvent

@dataclass
class TypingEventContent(SerializableAttrs['TypingEventContent']):
    user_ids: List[UserID]


@dataclass
class TypingEvent(BaseEvent, SerializableAttrs['TypingEvent']):
    room_id: RoomID
    content: TypingEventContent


class PresenceState(SerializableEnum):
    ONLINE = 'online'
    OFFLINE = 'offline'
    UNAVAILABLE = 'unavailable'


@dataclass
class PresenceEventContent(SerializableAttrs['PresenceEventContent']):
    presence: PresenceState
    last_active_ago: int = None
    status_msg: str = None
    currently_active: bool = None


@dataclass
class PresenceEvent(BaseEvent, SerializableAttrs['PresenceEvent']):
    sender: UserID
    content: PresenceEventContent


@dataclass
class SingleReceiptEventContent(SerializableAttrs['SingleReceiptEventContent']):
    ts: int


class ReceiptType(SerializableEnum):
    READ = 'm.read'


ReceiptEventContent = Dict[(EventID, Dict[(ReceiptType, Dict[(UserID, SingleReceiptEventContent)])])]

@dataclass
class ReceiptEvent(BaseEvent, SerializableAttrs['ReceiptEvent']):
    room_id: RoomID
    content: ReceiptEventContent