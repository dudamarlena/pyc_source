# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/users.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 778 bytes
from typing import List, NamedTuple
from attr import dataclass
from .event import Membership
from .primitive import UserID, ContentURI
from .util import SerializableAttrs

@dataclass
class Member(SerializableAttrs['Member']):
    membership: Membership = None
    avatar_url: ContentURI = None
    displayname: str = None


@dataclass
class User(SerializableAttrs['User']):
    user_id: UserID
    avatar_url: ContentURI = None
    displayname: str = None


UserSearchResults = NamedTuple('UserSearchResults', results=(List[User]), limit=int)