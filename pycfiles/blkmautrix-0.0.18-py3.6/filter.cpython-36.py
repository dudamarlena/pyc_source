# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/filter.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 6891 bytes
from typing import List
from attr import dataclass
from .util import SerializableAttrs, SerializableEnum
from .event import EventType
from .primitive import RoomID, UserID

class EventFormat(SerializableEnum):
    __doc__ = '\n    Federation event format enum, as specified in the `create filter endpoint`_.\n\n    .. _create filter endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-user-userid-filter\n    '
    CLIENT = 'client'
    FEDERATION = 'federation'


@dataclass
class EventFilter(SerializableAttrs['EventFilter']):
    __doc__ = "\n    Event filter object, as specified in the `create filter endpoint`_.\n\n    Attributes:\n        limit: The maximum number of events to return.\n        not_senders: A list of sender IDs to exclude. If this list is absent then no senders are\n            excluded. A matching sender will be excluded even if it is listed in the :attr:`senders`\n            filter.\n        not_types: A list of event types to exclude. If this list is absent then no event types are\n            excluded. A matching type will be excluded even if it is listed in the :attr:`types`\n            filter. A ``'*'`` can be used as a wildcard to match any sequence of characters.\n        senders: A list of senders IDs to include. If this list is absent then all senders are\n            included.\n        types: A list of event types to include. If this list is absent then all event types are\n            included. A ``'*'`` can be used as a wildcard to match any sequence of characters.\n\n    .. _create filter endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-user-userid-filter\n    "
    limit: int = None
    not_senders = None
    not_senders: List[UserID]
    not_types = None
    not_types: List[EventType]
    senders = None
    senders: List[UserID]
    types = None
    types: List[EventType]


@dataclass
class RoomEventFilter(EventFilter, SerializableAttrs['RoomEventFilter']):
    __doc__ = '\n    Room event filter object, as specified in the `create filter endpoint`_.\n\n    Attributes:\n        lazy_load_members: If ``True``, enables lazy-loading of membership events. See `Lazy-loading\n            room members`_ for more information.\n        include_redundant_members: If ``True``, sends all membership events for all events,\n            even if they have already been sent to the client. Does not apply unless\n            :attr:`lazy_load_members` is true. See `Lazy-loading room members`_ for more\n            information.\n        not_rooms: A list of room IDs to exclude. If this list is absent then no rooms are excluded.\n            A matching room will be excluded even if it is listed in the :attr:`rooms` filter.\n        rooms: A list of room IDs to include. If this list is absent then all rooms are included.\n        contains_url: If ``True``, includes only events with a url key in their content. If\n            ``False``, excludes those events. If omitted, ``url`` key is not considered for\n            filtering.\n\n    .. _create filter endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-user-userid-filter\n    .. _Lazy-loading room members:\n        https://matrix.org/docs/spec/client_server/r0.5.0#lazy-loading-room-members\n    '
    lazy_load_members: bool = False
    include_redundant_members: bool = False
    not_rooms = None
    not_rooms: List[RoomID]
    rooms = None
    rooms: List[RoomID]
    contains_url: bool = None


@dataclass
class StateFilter(RoomEventFilter, SerializableAttrs['RoomEventFilter']):
    __doc__ = '\n    State event filter object, as specified in the `create filter endpoint`_. Currently this is the\n    same as :class:`RoomEventFilter`.\n\n    .. _create filter endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-user-userid-filter\n    '


@dataclass
class RoomFilter(SerializableAttrs['RoomFilter']):
    __doc__ = "\n    Room filter object, as specified in the `create filter endpoint`_.\n\n    Attributes:\n        not_rooms: A list of room IDs to exclude. If this list is absent then no rooms are excluded.\n            A matching room will be excluded even if it is listed in the ``'rooms'`` filter. This\n            filter is applied before the filters in :attr:`ephemeral`, :attr:`state`,\n            :attr:`timeline` or :attr:`account_data`.\n        rooms: A list of room IDs to include. If this list is absent then all rooms are included.\n            This filter is applied before the filters in :attr:`ephemeral`, :attr:`state`,\n            :attr:`timeline` or :attr:`account_data`.\n        ephemeral: The events that aren't recorded in the room history, e.g. typing and receipts,\n            to include for rooms.\n        include_leave: Include rooms that the user has left in the sync.\n        state: The state events to include for rooms.\n        timeline: The message and state update events to include for rooms.\n        account_data: The per user account data to include for rooms.\n\n    .. _create filter endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-user-userid-filter\n    "
    not_rooms = None
    not_rooms: List[RoomID]
    rooms = None
    rooms: List[RoomID]
    ephemeral: RoomEventFilter = None
    include_leave: bool = False
    state: StateFilter = None
    timeline: RoomEventFilter = None
    account_data: RoomEventFilter = None


@dataclass
class Filter(SerializableAttrs['Filter']):
    __doc__ = "\n    Base filter object, as specified in the `create filter endpoint`_.\n\n    Attributes:\n        event_fields: List of event fields to include. If this list is absent then all fields are\n            included. The entries may include ``.`` charaters to indicate sub-fields. So\n            ``['content.body']`` will include the ``body`` field of the ``content`` object. A\n            literal ``.`` character in a field name may be escaped using a ``\\``. A server may\n            include more fields than were requested.\n        event_format: The format to use for events. ``'client'`` will return the events in a format\n            suitable for clients. ``'federation'`` will return the raw event as receieved over\n            federation. The default is :attr:`~EventFormat.CLIENT`.\n        presence: The presence updates to include.\n        account_data: The user account data that isn't associated with rooms to include.\n        room: Filters to be applied to room data.\n\n    .. _create filter endpoint:\n        https://matrix.org/docs/spec/client_server/r0.5.0#post-matrix-client-r0-user-userid-filter\n    "
    event_fields = None
    event_fields: List[str]
    event_format: EventFormat = None
    presence: EventFilter = None
    account_data: EventFilter = None
    room: RoomFilter = None