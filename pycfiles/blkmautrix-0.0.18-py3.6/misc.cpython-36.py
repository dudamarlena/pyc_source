# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/misc.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 2626 bytes
from enum import Enum
from typing import List, NewType, NamedTuple
from attr import dataclass
from .primitive import RoomID, RoomAlias, SyncToken, ContentURI
from .util import SerializableAttrs
from .event import Event

class RoomCreatePreset(Enum):
    __doc__ = '\n    Room creation preset, as specified in the `createRoom endpoint`_\n\n    .. _createRoom endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-createroom\n    '
    PRIVATE = 'private_chat'
    TRUSTED_PRIVATE = 'trusted_private_chat'
    PUBLIC = 'public_chat'


class RoomDirectoryVisibility(Enum):
    __doc__ = '\n    Room directory visibility, as specified in the `createRoom endpoint`_\n\n    .. _createRoom endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-createroom\n    '
    PRIVATE = 'private'
    PUBLIC = 'public'


class PaginationDirection(Enum):
    __doc__ = '\n    Pagination direction, as specified in the `pagination section`_.\n\n    .. _pagination section:\n        https://matrix.org/docs/spec/client_server/latest#pagination\n    '
    FORWARD = 'f'
    BACKWARD = 'b'


@dataclass
class RoomAliasInfo(SerializableAttrs['RoomAliasInfo']):
    __doc__ = '\n    Room alias query result, as specified in the `alias resolve endpoint`_\n\n    Attributes:\n        room_id: The room ID for this room alias.\n        servers: A list of servers that are aware of this room alias.\n\n    .. _alias resolve endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#get-matrix-client-r0-directory-room-roomalias\n    '
    room_id: RoomID = None
    servers = None
    servers: List[str]


DirectoryPaginationToken = NewType('DirectoryPaginationToken', str)

@dataclass
class PublicRoomInfo(SerializableAttrs['PublicRoomInfo']):
    room_id: RoomID
    num_joined_members: int
    world_readable: bool
    guests_can_join: bool
    name: str = None
    topic: str = None
    avatar_url: ContentURI = None
    aliases = None
    aliases: List[RoomAlias]
    canonical_alias: RoomAlias = None


@dataclass
class RoomDirectoryResponse(SerializableAttrs['RoomDirectoryResponse']):
    chunk: List[PublicRoomInfo]
    next_batch: DirectoryPaginationToken = None
    prev_batch: DirectoryPaginationToken = None
    total_room_count_estimate: int = None


PaginatedMessages = NamedTuple('PaginatedMessages', start=SyncToken, end=SyncToken, events=(List[Event]))