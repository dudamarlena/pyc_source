# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/event/account_data.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1682 bytes
from typing import Dict, Union
from attr import dataclass
import attr
from .....api import JSON
from ..util import SerializableAttrs, Obj, deserializer
from .base import EventType, BaseEvent

@dataclass
class RoomTagInfo(SerializableAttrs['RoomTagInfo']):
    order: int = None


@dataclass
class RoomTagAccountDataEventContent(SerializableAttrs['RoomTagAccountDataEventContent']):
    tags = attr.ib(default=None, metadata={'json': 'tags'})
    tags: Dict[(str, RoomTagInfo)]


AccountDataEventContent = Union[(RoomTagAccountDataEventContent, Obj)]
account_data_event_content_map = {EventType.TAG: RoomTagAccountDataEventContent}

@dataclass
class AccountDataEvent(BaseEvent, SerializableAttrs['AccountDataEvent']):
    content: AccountDataEventContent

    @classmethod
    def deserialize(cls, data):
        try:
            data.get('content', {})['__mautrix_event_type'] = EventType.find(data.get('type'))
        except ValueError:
            return Obj(**data)
        else:
            return super().deserialize(data)

    @staticmethod
    @deserializer(AccountDataEventContent)
    def deserialize_content(data: JSON) -> AccountDataEventContent:
        evt_type = data.pop('__mautrix_event_type', None)
        content_type = account_data_event_content_map.get(evt_type, None)
        if not content_type:
            return Obj(**data)
        else:
            return content_type.deserialize(data)