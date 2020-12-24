# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/types/json.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 1820 bytes
__doc__ = 'JSONType definition.'
import json, sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON, JSONB

class JSONType(sa.types.TypeDecorator):
    """JSONType"""
    impl = sa.UnicodeText

    def __init__(self, binary=True, impl=sa.UnicodeText, *args, **kwargs):
        self.binary = binary
        self.impl = impl
        (super().__init__)(*args, **kwargs)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            if self.binary:
                return dialect.type_descriptor(JSONB)
            else:
                return dialect.type_descriptor(JSON)
        else:
            return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        else:
            if value is not None:
                return json.dumps(value)
            return value

    def process_result_value(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        else:
            if value is not None:
                return json.loads(value)
            return value