# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/bridge/db/mx_user_profile.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1401 bytes
from typing import Optional
from sqlalchemy import Column, String, Enum, and_
from sqlalchemy.engine.result import RowProxy
from mautrix.types import RoomID, UserID, ContentURI, Member, Membership
from mautrix.util.db import Base

class UserProfile(Base):
    __tablename__ = 'mx_user_profile'
    room_id: RoomID = Column((String(255)), primary_key=True)
    user_id: UserID = Column((String(255)), primary_key=True)
    membership: Membership = Column((Enum(Membership)), nullable=False, default=(Membership.LEAVE))
    displayname: str = Column(String, nullable=True)
    avatar_url: ContentURI = Column((String(255)), nullable=True)

    def member(self) -> Member:
        return Member(membership=(self.membership), displayname=(self.displayname), avatar_url=(self.avatar_url))

    @classmethod
    def get(cls, room_id: RoomID, user_id: UserID) -> Optional['UserProfile']:
        return cls._select_one_or_none(and_(cls.c.room_id == room_id, cls.c.user_id == user_id))

    @classmethod
    def delete_all(cls, room_id: RoomID) -> None:
        with cls.db.begin() as (conn):
            conn.execute(cls.t.delete().where(cls.c.room_id == room_id))