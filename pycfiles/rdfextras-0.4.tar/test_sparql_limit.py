# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_limit.py
# Compiled at: 2012-02-24 05:27:21
import sys
from nose.exc import SkipTest
from rdflib import plugin
from rdflib.graph import ConjunctiveGraph
from rdflib.term import Literal
from rdflib.store import Store
from StringIO import StringIO
import unittest
test_data = ' \n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n<http://example.org/bob>  foaf:name       "Bob" .\n<http://example.org/dave>  foaf:name       "Dave" .\n<http://example.org/alice>  foaf:name       "Alice" .\n<http://example.org/charlie>  foaf:name       "Charlie" .\n'
test_query = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\nSELECT ?name\nWHERE { ?x foaf:name ?name . }\nLIMIT 2\n'
test_data2 = '\n@prefix dc: <http://purl.org/dc/elements/1.1/> .\n@prefix :   <http://example.org/book/> .\n@prefix ns: <http://example.org/ns#> .\n\n:book1 dc:title "SPARQL Tutorial" .\n:book1 ns:price 35 .\n:book2 dc:title "Python Tutorial" .\n:book2 ns:price 25 .\n:book3 dc:title "Java Tutorial" .\n:book3 ns:price 15 .\n:book3 dc:title "COBOL Tutorial" .\n:book3 ns:price 5 .\n'
test_query2 = '\nPREFIX dc: <http://purl.org/dc/elements/1.1/>\nPREFIX ns: <http://example.org/ns#>\n\nSELECT ?title ?price\nWHERE {\n ?x ns:price ?price .\n FILTER (?price < 20) .\n ?x dc:title ?title .\n}\nLIMIT 1'

class TestLimit(unittest.TestCase):

    def testLimit(self):
        graph = ConjunctiveGraph(plugin.get('IOMemory', Store)())
        graph.parse(data=test_data, format='n3')
        results = graph.query(test_query, DEBUG=False)
        print len(results)
        self.assertEqual(len(results), 2)

    def testLimit2(self):
        graph = ConjunctiveGraph(plugin.get('IOMemory', Store)())
        graph.parse(data=test_data2, format='n3')
        results = list(graph.query(test_query2, DEBUG=False))
        self.assertEqual(len(results), 1)
        for title, price in results:
            self.assertTrue(title in [Literal('Java Tutorial'),
             Literal('COBOL Tutorial')])


if __name__ == '__main__':
    unittest.main()