# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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