# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zuul/projects/neoalchemy/lib/python3.5/site-packages/neoalchemy/graph.py
# Compiled at: 2016-07-16 22:08:40
# Size of source mod 2**32: 5749 bytes
"""
A thin wrapper around the Neo4J Bolt driver's GraphDatabase class
providing a convenient auto-connection during initialization.
"""
from collections import deque, namedtuple
import warnings
from neo4j.v1 import GraphDatabase, basic_auth

class QueryLog(deque):
    MAX_SIZE = 100
    LogLine = namedtuple('LogLine', ('query', 'params'))

    def __init__(self, *args, **kw):
        super(QueryLog, self).__init__(*args, **kw)

    def __call__(self, query, params):
        self.append(self.LogLine(query=query, params=params))


class Query(object):
    __doc__ = 'Run queries on the Graph'

    def __init__(self, graph):
        self._Query__graph = graph
        self._Query__log = QueryLog()

    def __call__(self, q, **params):
        """Syntactic sugar for query.run(str(q), **params)"""
        return self.run(str(q), **params)

    @property
    def log(self):
        return self._Query__log

    def all(self):
        """MATCH (all) RETURN all"""
        return self.run('MATCH (all) RETURN all')

    def run(self, query, **params):
        """Run an arbitrary Cypher query"""
        with self._Query__graph.session() as (session):
            self.log(query, params)
            return session.run(query, parameters=params)


class Reflect(object):

    def __init__(self, graph):
        self._Reflect__graph = graph

    def constraints(self):
        """Fetch the current graph constraints"""
        constraints = self._Reflect__graph.query('CALL db.constraints()') or ()
        return (r['description'] for r in constraints)

    def indexes(self):
        """Fetch the current graph indexes"""
        indexes = self._Reflect__graph.query('CALL db.indexes()') or ()
        return (r['description'] for r in indexes)

    def labels(self):
        """Fetch the current graph labels"""
        labels = self._Reflect__graph.query('CALL db.labels()') or ()
        return (r['label'] for r in labels)


class Schema(object):

    def __init__(self, graph):
        self._Schema__graph = graph
        self._Schema__constraints = None
        self._Schema__indexes = None
        self._Schema__labels = None
        self._Schema__reflect = Reflect(graph)
        self._Schema__schema = set()

    def add(self, nodetype):
        """
        Add a NodeType to the schema, if not already present.
        """
        if nodetype.LABEL in self._Schema__schema:
            return
        self._Schema__schema.add(nodetype.LABEL)
        schema = self.indexes() + self.constraints()
        for index_or_constraint in nodetype.schema:
            if index_or_constraint not in schema:
                self._Schema__graph.query('CREATE ' + index_or_constraint)

    def constraints(self):
        """
        Get current graph constraints lazily.

        On first access, this fetches from the database. Afterwards, call
        update() to refresh.
        """
        if self._Schema__constraints is None:
            self._Schema__constraints = tuple(self._Schema__reflect.constraints())
        return self._Schema__constraints

    def indexes(self):
        """
        Get current graph indexes lazily.

        On first access, this fetches from the database. Afterwards, call
        update() to refresh.
        """
        if self._Schema__indexes is None:
            self._Schema__indexes = tuple(self._Schema__reflect.indexes())
        return self._Schema__indexes

    def labels(self):
        """
        Get current graph labels lazily.

        On first access, this fetches from the database. Afterwards, call
        update() to refresh.
        """
        if self._Schema__labels is None:
            self._Schema__labels = tuple(self._Schema__reflect.labels())
        return self._Schema__labels

    @property
    def ls(self):
        """Cypher statements for currently defined schema"""
        return '\n'.join(self.indexes() + self.constraints())

    def update(self):
        """Refresh graph constraints, indexes, and labels"""
        self._Schema__constraints = tuple(self._Schema__reflect.constraints())
        self._Schema__indexes = tuple(self._Schema__reflect.indexes())
        self._Schema__labels = tuple(self._Schema__reflect.labels())
        return self


class Graph(GraphDatabase):
    __doc__ = "\n    A thin wrapper around the Neo4J Bolt driver's GraphDatabase class\n    providing a convenient auto-connection during initialization.\n    "

    def __init__(self, url=None, **kw):
        self.connect(url, **kw)
        self._Graph__query = Query(self)
        self._Graph__schema = Schema(self)

    @property
    def query(self):
        return self._Graph__query

    @property
    def schema(self):
        return self._Graph__schema

    def connect(self, url=None, user=None, password=None):
        """
        Parse a Neo4J URL and attempt to connect using Bolt

        Note: If the user and password arguments are provided, they
        will only be used in case no auth information is provided as
        part of the connection URL.
        """
        if url is None:
            url = 'bolt://localhost'
        if user is None:
            user = 'neo4j'
        if password is None:
            password = 'neo4j'
        try:
            protocol, url = url.split('://')
            if protocol.lower() != 'bolt':
                warnings.warn('Switching protocols. Only Bolt is supported.')
        except ValueError:
            pass

        try:
            credentials, url = url.split('@')
        except ValueError:
            auth_token = basic_auth(user, password)
        else:
            auth_token = basic_auth(*credentials.split(':', 1))
        self.driver = GraphDatabase.driver('bolt://%s' % url, auth=auth_token)

    def delete_all(self):
        """MATCH (all) DETACH DELETE all"""
        with self.session() as (session):
            session.run('MATCH (all) DETACH DELETE all')

    def session(self):
        """Syntactic sugar for graph.driver.session()"""
        return self.driver.session()