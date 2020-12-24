# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/aiogql/transport/local_schema.py
# Compiled at: 2020-01-21 09:02:42
# Size of source mod 2**32: 310 bytes
from graphql.execution import execute

class LocalSchemaTransport(object):

    def __init__(self, schema):
        self.schema = schema

    def execute(self, document, *args, **kwargs):
        return execute(
 self.schema,
 document, *args, **kwargs)