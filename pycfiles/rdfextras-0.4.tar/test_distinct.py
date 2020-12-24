# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_distinct.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from StringIO import StringIO
import unittest, rdflib
from rdflib import Literal
test_data = '\n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n_:a  foaf:name       "Alice" .\n_:a  foaf:surName      "Carol" . \n_:a  foaf:lastName      "Carol" . \n\n_:b  foaf:name       "Alice" . \n\n_:c  foaf:surName "Emerson" .\n\n_:d  foaf:surName "Emerson" .\n'
test_query_literal = 'PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nSELECT DISTINCT ?x\nWHERE {\n    ?y foaf:name ?x .\n}'
test_query_resource = "PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nSELECT DISTINCT ?x\nWHERE {\n    ?x ?p 'Carol' .\n}"
test_query_order = 'PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nSELECT DISTINCT ?name\nWHERE {\n    ?x foaf:surName ?name . \n} ORDER by ?name\n'

class Query(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.parse(StringIO(test_data), format='n3')

    def testQuery1(self):
        r = list(self.graph.query(test_query_literal))
        print r
        self.assertEqual(len(r), 1)

    def testQuery2(self):
        r = list(self.graph.query(test_query_resource))
        print r
        self.assertEqual(len(r), 1)

    def testQuery3(self):
        r = list(self.graph.query(test_query_order))
        print r
        self.assertEqual(list(r), [(Literal('Carol'),), (Literal('Emerson'),)])


if __name__ == '__main__':
    unittest.main()