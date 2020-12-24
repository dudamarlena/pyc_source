# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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