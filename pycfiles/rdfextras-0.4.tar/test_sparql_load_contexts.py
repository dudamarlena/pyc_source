# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_load_contexts.py
# Compiled at: 2012-04-24 09:28:08
from urllib2 import URLError
try:
    from Ft.Lib import UriException
except:
    from urllib2 import URLError as UriException

import unittest
from rdflib import ConjunctiveGraph, URIRef

class SPARQLloadContextsTest(unittest.TestCase):

    def test_dSet_parsed_as_URL_raises_Exception(self):
        querystr = 'SELECT DISTINCT ?s FROM <http://test/> { ?s ?p ?o }'
        graph = ConjunctiveGraph()
        graph.get_context(URIRef('http://test/')).parse('http://www.w3.org/People/Berners-Lee/card.rdf')
        self.assertRaises((URLError, UriException), graph.query, querystr, loadContexts=False)

    def test_dSet_parsed_as_context_returns_results(self):
        querystr = 'SELECT DISTINCT ?s FROM <http://test/> { ?s ?p ?o }'
        graph = ConjunctiveGraph()
        graph.get_context(URIRef('http://test/')).parse('http://www.w3.org/People/Berners-Lee/card.rdf')
        r = graph.query(querystr, loadContexts=True)
        self.assert_(len(r.bindings) is not 0)