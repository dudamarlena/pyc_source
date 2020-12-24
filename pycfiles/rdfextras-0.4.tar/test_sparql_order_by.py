# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_order_by.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from rdflib import plugin, query
from rdflib.term import Literal
from rdflib.store import Store
from StringIO import StringIO
import unittest
test_data = ' \n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n<http://example.org/bob>  foaf:name       "Bob" .\n<http://example.org/dave>  foaf:name       "Dave" .\n<http://example.org/alice>  foaf:name       "Alice" .\n<http://example.org/charlie>  foaf:name       "Charlie" .\n'
test_query = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\nSELECT ?name\nWHERE { ?x foaf:name ?name . }\nORDER BY ?name\n'

class TestOrderBy(unittest.TestCase):

    def testOrderBy(self):
        graph = ConjunctiveGraph(plugin.get('IOMemory', Store)())
        graph.parse(StringIO(test_data), format='n3')
        results = graph.query(test_query)
        self.failUnless(False not in [ r[0] == a for r, a in zip(results, ['Alice', 'Bob', 'Charlie', 'Dave']) ])


if __name__ == '__main__':
    unittest.main()