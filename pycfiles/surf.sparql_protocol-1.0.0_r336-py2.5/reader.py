# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparql_protocol/reader.py
# Compiled at: 2011-04-12 03:29:53
__author__ = 'Cosmin Basca'
import sys
from SPARQLWrapper import SPARQLWrapper, jsonlayer, JSON
from SPARQLWrapper.SPARQLExceptions import EndPointNotFound, QueryBadFormed
from surf.util import json_to_rdflib
from surf.plugin.query_reader import RDFQueryReader
from surf.rdf import BNode, ConjunctiveGraph, Literal, URIRef

class SparqlReaderException(Exception):
    pass


class ReaderPlugin(RDFQueryReader):

    def __init__(self, *args, **kwargs):
        RDFQueryReader.__init__(self, *args, **kwargs)
        self.__endpoint = kwargs['endpoint'] if 'endpoint' in kwargs else None
        self.__results_format = JSON
        self.__sparql_wrapper = SPARQLWrapper(self.__endpoint, self.__results_format)
        if kwargs.get('use_keepalive', '').lower().strip() == 'true':
            if hasattr(SPARQLWrapper, 'setUseKeepAlive'):
                self.__sparql_wrapper.setUseKeepAlive()
        return

    endpoint = property(lambda self: self.__endpoint)
    results_format = property(lambda self: self.__results_format)

    def _to_table(self, result):
        if not isinstance(result, dict):
            return result
        if 'results' not in result:
            return result
        converted = []
        for binding in result['results']['bindings']:
            rdf_item = {}
            for (key, obj) in binding.items():
                try:
                    rdf_item[key] = json_to_rdflib(obj)
                except ValueError:
                    continue

            converted.append(rdf_item)

        return converted

    def _ask(self, result):
        """
        returns the boolean value of a ASK query
        """
        return result.get('boolean')

    def execute_sparql(self, q_string, format='JSON'):
        try:
            self.log.debug(q_string)
            self.__sparql_wrapper.setQuery(q_string)
            return self.__sparql_wrapper.query().convert()
        except EndPointNotFound, _:
            raise SparqlReaderException('Endpoint not found'), None, sys.exc_info()[2]
        except QueryBadFormed, _:
            raise SparqlReaderException('Bad query: %s' % q_string), None, sys.exc_info()[2]
        except Exception, e:
            raise SparqlReaderException('Exception: %s' % e), None, sys.exc_info()[2]

        return

    def _execute(self, query):
        return self.execute_sparql(unicode(query))

    def close(self):
        pass