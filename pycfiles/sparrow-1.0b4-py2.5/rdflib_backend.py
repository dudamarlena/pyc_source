# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/rdflib_backend.py
# Compiled at: 2009-07-20 09:57:48
from cStringIO import StringIO
from zope.interface import implements
try:
    import rdflib
    from rdflib.Graph import Graph, ConjunctiveGraph
    from rdflib.store.IOMemory import IOMemory
except ImportError:
    rdflib = None

from sparrow.base_backend import BaseBackend
from sparrow.error import ConnectionError, TripleStoreError, QueryError
from sparrow.interfaces import ITripleStore, ISPARQLEndpoint
from sparrow.utils import parse_sparql_result, dict_to_ntriples, ntriples_to_dict, json_to_ntriples, ntriples_to_json

class RDFLibTripleStore(BaseBackend):
    implements(ITripleStore, ISPARQLEndpoint)

    def __init__(self):
        self._nsmap = {}

    def connect(self, dburi):
        if rdflib is None:
            raise ConnectionError('RDFLib backend is not installed')
        if dburi == 'memory':
            self._store = IOMemory()
        else:
            raise ConnectionError('Unknown database config: %s' % dburi)
        return

    def disconnect(self):
        pass

    def _rdflib_format(self, format):
        return {'ntriples': 'nt', 'rdfxml': 'xml', 
           'turtle': 'n3'}[format]

    def contexts(self):
        return [ c._Graph__identifier.decode('utf8') for c in self._store.contexts()
               ]

    def _get_context(self, context_name):
        for ctxt in self._store.contexts():
            if ctxt._Graph__identifier == context_name:
                return ctxt

    def register_prefix(self, prefix, namespace):
        self._nsmap[prefix] = namespace

    def _parse(self, graph, file, format, base_uri=None):
        try:
            graph.parse(file, base_uri, format)
        except rdflib.exceptions.ParserError, err:
            raise TripleStoreError(err)
        except Exception, err:
            raise TripleStoreError(err)

    def add_rdfxml(self, data, context, base_uri):
        data = self._get_file(data)
        graph = Graph(self._store, identifier=context)
        self._parse(graph, data, 'xml', base_uri)

    def add_ntriples(self, data, context):
        data = self._get_file(data)
        graph = Graph(self._store, identifier=context)
        self._parse(graph, data, 'nt')

    def add_turtle(self, data, context):
        data = self._get_file(data)
        graph = Graph(self._store, identifier=context)
        self._parse(graph, data, 'n3')

    def _serialize(self, graph, format, pretty=False):
        for (prefix, namespace) in self._nsmap.items():
            graph.bind(prefix, namespace)

        return StringIO(graph.serialize(format=format))

    def get_rdfxml(self, context, pretty=False):
        return self._serialize(self._get_context(context), 'xml')

    def get_turtle(self, context):
        return self._serialize(self._get_context(context), 'n3')

    def get_ntriples(self, context):
        return self._serialize(self._get_context(context), 'nt')

    def remove_rdfxml(self, data, context, base_uri):
        data = self._get_file(data)
        self._remove(data, context, 'xml', base_uri)

    def remove_ntriples(self, data, context):
        data = self._get_file(data)
        self._remove(data, context, 'nt')

    def remove_turtle(self, data, context):
        data = self._get_file(data)
        self._remove(data, context, 'n3')

    def _remove(self, file, context, format, base_uri=None):
        graph = Graph()
        self._parse(graph, file, format=format, base_uri=base_uri)
        context = self._get_context(context)
        for triple in graph:
            self._store.remove(triple, context)

    def clear(self, context):
        context = self._get_context(context)
        self._store.remove((None, None, None), context)
        return

    def count(self, context=None):
        context = self._get_context(context)
        if context is not None:
            return len(context)
        return len(self._store)

    def _query(self, sparql):
        try:
            result = ConjunctiveGraph(self._store).query(sparql)
        except SyntaxError, err:
            raise QueryError(err)

        return result

    def select(self, sparql):
        result = self._query(sparql)
        return parse_sparql_result(result.serialize())

    def ask(self, sparql):
        result = self._query(sparql)
        return result.askAnswer[0]

    def construct(self, sparql, format):
        out_format = format
        if format in ('json', 'dict'):
            out_format = 'ntriples'
        result = self._query(sparql)
        if not result.construct:
            raise QueryError('CONSTRUCT Query did not return a graph')
        result = self._serialize(result.result, self._rdflib_format(out_format))
        if format == 'json':
            result = ntriples_to_json(result)
        elif format == 'dict':
            result = ntriples_to_dict(result)
        return result