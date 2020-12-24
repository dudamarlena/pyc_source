# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/types/uuid.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 2119 bytes
import uuid
from sqlalchemy import types
from sqlalchemy.dialects import postgresql
from .choice import ScalarCoercible

class UUIDType(types.TypeDecorator, ScalarCoercible):
    """UUIDType"""
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