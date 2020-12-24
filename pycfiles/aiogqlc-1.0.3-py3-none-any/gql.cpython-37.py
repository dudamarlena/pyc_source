# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/aiogql/gql.py
# Compiled at: 2020-01-21 09:02:42
# Size of source mod 2**32: 360 bytes
import six
from graphql.language.parser import parse
from graphql.language.source import Source

def gql(request_string):
    if isinstance(request_string, six.string_types):
        source = Source(request_string, 'GraphQL request')
        return parse(source)
    raise Exception('Received incompatible request "{}".'.format(request_string))