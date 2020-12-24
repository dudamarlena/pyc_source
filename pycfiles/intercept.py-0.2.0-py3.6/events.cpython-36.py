# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intercept/events.py
# Compiled at: 2018-12-27 16:24:21
# Size of source mod 2**32: 1803 bytes
from dataclasses import field, dataclass
from typing import Any, Dict
from intercept.utils import REGEXES

@dataclass
class Event:
    event: str


@dataclass
class MessageEvent(Event):
    event: str
    msg: str


@dataclass
class InfoEvent(Event):
    event: str
    client_id: str
    client_type: str
    connected_at: int
    date: int


@dataclass
class AuthEvent(Event):
    event: str
    success: bool
    token: str
    cfg: dict


@dataclass
class ConnectData:
    ip: str
    conn: str


@dataclass
class ConnectEvent(MessageEvent):
    event: str
    success: bool
    msg: str
    player: ConnectData
    cfg = field(default_factory=dict)
    cfg: Dict[(str, Any)]


@dataclass
class CommandEvent(MessageEvent):
    event: str
    success: bool
    cmd: str
    msg: str


@dataclass
class ConnectedEvent(Event):
    event: str
    player: ConnectData


@dataclass
class BroadcastEvent(MessageEvent):
    event: str
    msg: str


@dataclass
class TraceStartEvent(MessageEvent):
    event: str
    system: str
    panic: bool
    msg: str


@dataclass
class TraceCompleteEvent(MessageEvent):
    event: str
    system: str
    panicEnd: bool
    msg: str


@dataclass
class ChatEvent(MessageEvent):
    event: str
    msg: str

    @property
    def chat(self) -> str:
        return REGEXES['chat_event'].match(self.msg).group('chat')

    @property
    def author(self) -> str:
        return REGEXES['chat_event'].match(self.msg).group('author')

    @property
    def message(self) -> str:
        return REGEXES['chat_event'].match(self.msg).group('message')


@dataclass
class ErrorEvent(Event):
    event: str
    success: bool
    error: str


@dataclass
class ConfigEvent(Event):
    event: str
    cfg = field(default_factory=dict)
    cfg: Dict[(str, Any)]