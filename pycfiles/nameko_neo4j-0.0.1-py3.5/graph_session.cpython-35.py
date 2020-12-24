# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/nameko_neo4j/graph_session.py
# Compiled at: 2017-02-01 10:27:43
# Size of source mod 2**32: 580 bytes
from py2neo import Graph, authenticate
from nameko.extensions import DependencyProvider

class GraphSession(DependencyProvider):

    def setup(self):
        self.db_username = self.container.config['DATABASE']['USERNAME']
        self.db_password = self.container.config['DATABASE']['PASSWORD']
        self.db_url = self.container.config['DATABASE']['URL']
        self.db_endpoint = self.container.config['DATABASE']['ENDPOINT']

    def get_dependency(self):
        authenticate(self.db_url, self.db_username, self.db_password)
        self.graph = Graph(self.db_endpoint)