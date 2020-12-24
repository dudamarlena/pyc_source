# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/admin.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 867 bytes
import click
from . import helpers
from .graphql import GraphQL
from .helpers import config_string
DEFAULT_GRAPHQL_ADMIN = 'http://127.0.0.1:5001/graphql'
graphql_admin_option = [click.option('--graphql-admin', help='GraphQL endpoint', default=DEFAULT_GRAPHQL_ADMIN, callback=config_string, show_default=True)]

class Admin(GraphQL):

    @helpers.timeit
    def __init__(self, graphql=None):
        graphql = graphql if graphql is not None else DEFAULT_GRAPHQL_ADMIN
        GraphQL.__init__(self, graphql=graphql)

    @helpers.timeit
    def users(self):
        query = '{\n            accountsList {\n                user {\n                  lastName\n                  createdAt\n                  updatedAt\n                  firstName\n                }\n                email\n            }\n        }'
        return self._post(query)['data']['accountsList']