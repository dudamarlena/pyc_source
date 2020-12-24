# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/pkg/compressed_json_type.py
# Compiled at: 2018-09-29 23:45:54
# Size of source mod 2**32: 3012 bytes
from __future__ import absolute_import
import six, zlib, sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import ischema_names
json = None
try:
    import anyjson as json
except ImportError:
    import json

try:
    from sqlalchemy.dialects.postgresql import JSON
    has_postgres_json = True
except ImportError:

    class PostgresJSONType(sa.types.UserDefinedType):
        __doc__ = '\n        Text search vector type for postgresql.\n        '

        def get_col_spec(self):
            return 'json'


    ischema_names['json'] = PostgresJSONType
    has_postgres_json = False

class CompressedJSONType(sa.types.TypeDecorator):
    __doc__ = "\n    JSONType offers way of saving JSON data structures to database. On\n    PostgreSQL the underlying implementation of this data type is 'json' while\n    on other databases its simply 'text'.\n\n    ::\n\n\n        from sqlalchemy_utils import JSONType\n\n\n        class Product(Base):\n            __tablename__ = 'product'\n            id = sa.Column(sa.Integer, autoincrement=True)\n            name = sa.Column(sa.Unicode(50))\n            details = sa.Column(JSONType)\n\n\n        product = Product()\n        product.details = {\n            'color': 'red',\n            'type': 'car',\n            'max-speed': '400 mph'\n        }\n        session.commit()\n    "
    impl = sa.LargeBinary

    def __init__(self, *args, **kwargs):
        (super(CompressedJSONType, self).__init__)(*args, **kwargs)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            if has_postgres_json:
                return dialect.type_descriptor(JSON())
            else:
                return dialect.type_descriptor(PostgresJSONType())
        else:
            return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        if dialect.name == 'postgresql':
            if has_postgres_json:
                return value
        if value is not None:
            value = six.binary_type(zlib.compress(json.dumps(value).encode('utf-8')))
        return value

    def process_result_value(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        else:
            if value is not None:
                value = json.loads(zlib.decompress(value).decode('utf-8'))
            return value


if __name__ == '__main__':
    from sqlalchemy import MetaData, Table, Column, Integer, select
    from uszipcode.packages.sqlalchemy_mate import engine_creator
    engine = engine_creator.create_sqlite()
    metadata = MetaData()
    t_user = Table('user', metadata, Column('id', Integer), Column('profile', CompressedJSONType))
    metadata.create_all(engine)
    engine.execute(t_user.insert(), {'id':1,  'profile':{'lastname':'John', 
      'firstname':'David'}})
    user_data = engine.execute(select([t_user])).fetchone()
    if not user_data['profile'] == {'lastname':'John',  'firstname':'David'}:
        raise AssertionError