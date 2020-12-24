# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/broker/model/types.py
# Compiled at: 2016-06-27 03:37:38
# Size of source mod 2**32: 2357 bytes
from sqlalchemy.types import TypeDecorator
from sqlalchemy.types import CHAR
from sqlalchemy.types import TEXT
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.postgresql import ARRAY

class UUID(TypeDecorator):
    __doc__ = "Platform-independent GUID type.\n\n    This type returns an Unicode string: the GUID\n    encoded in hexadecimal with no dashes.\n\n    Uses Postgresql's UUID type, otherwise uses\n    CHAR(32), storing as stringified hex values.\n\n    "
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
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return value.replace('-', '')


class UUIDArray(TypeDecorator):
    __doc__ = "Platform-independent GUID array type.\n\n    This type returns an array of Unicode strings.\n    Each GUID is encoded in hexadecimal with no dashes.\n\n    Uses Postgresql's UUID and ARRAY types, otherwise\n    uses TEXT, storing as stringified hex values.\n    "
    impl = CHAR

    def __init__(self, *a, remove_null=False, **k):
        self.remove_null = remove_null
        super(UUIDArray, self).__init__(*a, **k)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(ARRAY(PG_UUID()))
        else:
            return dialect.type_descriptor(TEXT)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            return '{{{}}}'.format(','.join(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if dialect.name == 'postgresql':
                value = ''.join(value)
            res = value.strip('{}').replace('-', '').split(',')
            if len(res) == 1 and res[0] == '':
                return []
            if self.remove_null:
                return list(filter(lambda x: x != 'NULL', res))
            return res