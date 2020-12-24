# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/schemas/schema.py
# Compiled at: 2020-05-09 07:13:20
# Size of source mod 2**32: 428 bytes
from marshmallow import Schema

def camelcase(s):
    parts = iter(s.split('_'))
    return next(parts) + ''.join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    __doc__ = 'Schema that uses camel-case for its external representation\n    and snake-case for its internal representation.\n    '

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)