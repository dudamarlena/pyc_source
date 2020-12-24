# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/event/redaction.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1115 bytes
from typing import Optional
from attr import dataclass
import attr
from ..util import SerializableAttrs
from ..primitive import EventID
from .base import BaseRoomEvent, BaseUnsigned

@dataclass
class RedactionEventContent(SerializableAttrs['RedactionEventContent']):
    __doc__ = 'The content of an m.room.redaction event'
    reason: str = None


@dataclass
class RedactionEvent(BaseRoomEvent, SerializableAttrs['RedactionEvent']):
    __doc__ = 'A m.room.redaction event'
    content: RedactionEventContent
    redacts: EventID
    _unsigned = attr.ib(default=None, metadata={'json': 'unsigned'})
    _unsigned: Optional[BaseUnsigned]

    @property
    def unsigned(self) -> BaseUnsigned:
        if not self._unsigned:
            self._unsigned = BaseUnsigned()
        return self._unsigned

    @unsigned.setter
    def unsigned(self, value: BaseUnsigned) -> None:
        self._unsigned = value