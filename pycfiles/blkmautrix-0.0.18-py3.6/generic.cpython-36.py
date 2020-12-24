# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/event/generic.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 2890 bytes
from typing import Union, NewType, Optional
from attr import dataclass
from mautrix.api import JSON
from ..primitive import RoomID, EventID, UserID
from ..util import deserializer, Obj, SerializableAttrs
from .base import EventType, BaseEvent
from .redaction import RedactionEvent, RedactionEventContent
from .message import MessageEvent, MessageEventContent
from .reaction import ReactionEvent, ReactionEventContent
from .state import StateEvent, StateEventContent
from .account_data import AccountDataEvent, AccountDataEventContent
from .ephemeral import ReceiptEvent, PresenceEvent, TypingEvent, ReceiptEventContent, TypingEventContent

@dataclass
class GenericEvent(BaseEvent, SerializableAttrs['GenericEvent']):
    __doc__ = "\n    An event class that contains all possible top-level event keys and uses generic Obj's for object\n    keys (content and unsigned)\n    "
    content: Obj
    type: EventType
    room_id = None
    room_id: Optional[RoomID]
    event_id = None
    event_id: Optional[EventID]
    sender = None
    sender: Optional[UserID]
    timestamp = None
    timestamp: Optional[int]
    state_key = None
    state_key: Optional[str]
    unsigned: Obj = None
    readacts = None
    readacts: Optional[EventID]


Event = NewType('Event', Union[(MessageEvent, ReactionEvent, RedactionEvent, StateEvent, ReceiptEvent,
 PresenceEvent, TypingEvent, GenericEvent)])
EventContent = Union[(MessageEventContent, RedactionEventContent, ReactionEventContent,
 StateEventContent, AccountDataEventContent, ReceiptEventContent,
 TypingEventContent, Obj)]

@deserializer(Event)
def deserialize_event(data: JSON) -> Event:
    event_type = EventType.find(data.get('type', None))
    if event_type == EventType.ROOM_MESSAGE:
        return MessageEvent.deserialize(data)
    if event_type == EventType.STICKER:
        data.get('content', {})['msgtype'] = 'm.sticker'
        return MessageEvent.deserialize(data)
    if event_type == EventType.REACTION:
        return ReactionEvent.deserialize(data)
    if event_type == EventType.ROOM_REDACTION:
        return RedactionEvent.deserialize(data)
    if event_type.is_state:
        return StateEvent.deserialize(data)
    if event_type.is_account_data:
        return AccountDataEvent.deserialize(data)
    if event_type == EventType.RECEIPT:
        return ReceiptEvent.deserialize(data)
    if event_type == EventType.TYPING:
        return TypingEvent.deserialize(data)
    else:
        if event_type == EventType.PRESENCE:
            return PresenceEvent.deserialize(data)
        return GenericEvent.deserialize(data)


setattr(Event, 'deserialize', deserialize_event)