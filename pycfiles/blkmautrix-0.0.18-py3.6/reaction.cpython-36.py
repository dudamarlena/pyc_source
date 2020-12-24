# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/event/reaction.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1434 bytes
from typing import Optional
from attr import dataclass
import attr
from ..util import SerializableAttrs
from .base import BaseRoomEvent, BaseUnsigned
from .message import RelatesTo

@dataclass
class ReactionEventContent(SerializableAttrs['ReactionEventContent']):
    __doc__ = 'The content of an m.reaction event'
    _relates_to = attr.ib(default=None, metadata={'json': 'm.relates_to'})
    _relates_to: Optional[RelatesTo]

    @property
    def relates_to(self) -> RelatesTo:
        if self._relates_to is None:
            self._relates_to = RelatesTo()
        return self._relates_to

    @relates_to.setter
    def relates_to(self, relates_to: RelatesTo) -> None:
        self._relates_to = relates_to


@dataclass
class ReactionEvent(BaseRoomEvent, SerializableAttrs['ReactionEvent']):
    __doc__ = 'A m.reaction event'
    content: ReactionEventContent
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