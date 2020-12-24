# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/types/uuid.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 2119 bytes
import uuid
from sqlalchemy import types
from sqlalchemy.dialects import postgresql
from .choice import ScalarCoercible

class UUIDType(types.TypeDecorator, ScalarCoercible):
    __doc__ = "\n    Stores a UUID in the database natively when it can and falls back to\n    a BINARY(16) or a CHAR(32) when it can't.\n\n    ::\n\n        from odm.types import UUIDType\n        import uuid\n\n        class User(Base):\n            __tablename__ = 'user'\n\n            # Pass `binary=False` to fallback to CHAR instead of BINARY\n            id = sa.Column(UUIDType(binary=False), primary_key=True)\n    "
    impl = types.BINARY(16)
    python_type = uuid.UUID

    def __init__(self, binary=True, native=True, **kwargs):
        """
        :param binary: Whether to use a BINARY(16) or CHAR(32) fallback.
        """
        self.binary = binary
        self.native = native

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            if self.native:
                return dialect.type_descriptor(postgresql.UUID())
        kind = self.impl if self.binary else types.CHAR(32)
        return dialect.type_descriptor(kind)

    @staticmethod
    def _coerce(value):
        if value:
            if not isinstance(value, uuid.UUID):
                try:
                    value = uuid.UUID(value)
                except (TypeError, ValueError):
                    value = uuid.UUID(bytes=value)

        return value

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = self._coerce(value)
            else:
                if self.native:
                    if dialect.name == 'postgresql':
                        return str(value)
                if self.binary:
                    return value.bytes
            return value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if self.native:
                if dialect.name == 'postgresql':
                    return uuid.UUID(value)
            if self.binary:
                return uuid.UUID(bytes=value)
            return uuid.UUID(value)