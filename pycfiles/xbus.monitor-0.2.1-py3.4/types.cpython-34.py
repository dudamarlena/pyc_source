# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/models/types.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 1043 bytes
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

class UUID(TypeDecorator):
    __doc__ = "Platform-independent GUID type.\n\n    Uses Postgresql's UUID type, otherwise uses\n    CHAR(32), storing as stringified hex values.\n\n    "
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if dialect.name == 'postgresql':
                return str(value)
            if not isinstance(value, uuid.UUID):
                return '%.32x' % uuid.UUID(value)
            return '%.32x' % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)