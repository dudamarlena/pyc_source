# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/bridge/db/mx_room_state.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 1520 bytes
from typing import Dict, Optional
import json
from sqlalchemy import Column, String, types
from mautrix.types import RoomID, PowerLevelStateEventContent
from mautrix.util.db import Base

class PowerLevelType(types.TypeDecorator):
    impl = types.Text

    @property
    def python_type(self):
        return PowerLevelStateEventContent

    def process_bind_param(self, value: PowerLevelStateEventContent, dialect) -> Optional[Dict]:
        if value is not None:
            return json.dumps(value.serialize())

    def process_result_value(self, value: Dict, dialect) -> Optional[PowerLevelStateEventContent]:
        if value is not None:
            return PowerLevelStateEventContent.deserialize(json.loads(value))

    def process_literal_param(self, value, dialect):
        return value


class RoomState(Base):
    __tablename__ = 'mx_room_state'
    room_id: RoomID = Column((String(255)), primary_key=True)
    power_levels: PowerLevelStateEventContent = Column(PowerLevelType, nullable=True)

    @property
    def has_power_levels(self) -> bool:
        return bool(self.power_levels)

    @classmethod
    def get(cls, room_id: RoomID) -> Optional['RoomState']:
        return cls._select_one_or_none(cls.c.room_id == room_id)