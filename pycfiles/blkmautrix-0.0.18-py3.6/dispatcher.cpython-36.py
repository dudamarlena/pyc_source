# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/dispatcher.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 2248 bytes
from abc import ABC, abstractmethod
import asyncio
from .api.types import EventType, StateEvent, Membership
from .client import Client, InternalEventType, SyncStream

class Dispatcher(ABC):
    client: Client

    def __init__(self, client: Client) -> None:
        self.client = client

    @abstractmethod
    def register(self) -> None:
        pass

    @abstractmethod
    def unregister(self) -> None:
        pass

    def _dispatch(self, event_type: InternalEventType, evt: StateEvent) -> None:
        asyncio.ensure_future((self.client.dispatch_manual_event(event_type, evt)), loop=(self.client.loop))


class MembershipEventDispatcher(Dispatcher):

    def register(self) -> None:
        self.client.add_event_handler(EventType.ROOM_MEMBER, self.handle)

    def unregister(self) -> None:
        self.client.remove_event_handler(EventType.ROOM_MEMBER, self.handle)

    async def handle(self, evt: StateEvent) -> None:
        if evt.type != EventType.ROOM_MEMBER:
            return
        if evt.content.membership == Membership.JOIN:
            if evt.prev_content.membership != Membership.JOIN:
                self._dispatch(InternalEventType.JOIN, evt)
            else:
                self._dispatch(InternalEventType.PROFILE_CHANGE, evt)
        else:
            if evt.content.membership == Membership.INVITE:
                self._dispatch(InternalEventType.INVITE, evt)
            else:
                if evt.content.membership == Membership.LEAVE:
                    if evt.state_key == evt.sender:
                        self._dispatch(InternalEventType.LEAVE, evt)
                    else:
                        if evt.prev_content.membership == Membership.BAN:
                            self._dispatch(InternalEventType.UNBAN, evt)
                        else:
                            if evt.prev_content.membership == Membership.INVITE:
                                self._dispatch(InternalEventType.DISINVITE, evt)
                            else:
                                self._dispatch(InternalEventType.KICK, evt)
                elif evt.content.membership == Membership.BAN:
                    self._dispatch(InternalEventType.BAN, evt)