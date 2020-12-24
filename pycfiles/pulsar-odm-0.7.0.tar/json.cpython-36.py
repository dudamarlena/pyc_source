# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/types/json.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 1820 bytes
"""JSONType definition."""
import json, sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON, JSONB

class JSONType(sa.types.TypeDecorator):
    __doc__ = "\n    JSONType offers way of saving JSON data structures to database. On\n    PostgreSQL the underlying implementation of this data type is 'json' while\n    on other databases its simply 'text'.\n\n    ::\n\n\n        from odm.types import JSONType\n\n\n        class Product(Base):\n            __tablename__ = 'product'\n            id = sa.Column(sa.Integer, autoincrement=True)\n            name = sa.Column(sa.Unicode(50))\n            details = sa.Column(JSONType)\n\n\n        product = Product()\n        product.details = {\n            'color': 'red',\n            'type': 'car',\n            'max-speed': '400 mph'\n        }\n        session.commit()\n    "
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