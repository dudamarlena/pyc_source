# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_empty_prefix.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from StringIO import StringIO
import unittest, rdflib
test_data = '\n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n_:a  foaf:name       "Alice" .\n'
test_query = 'PREFIX :<http://xmlns.com/foaf/0.1/>\nSELECT ?name\nWHERE {\n    ?x :name ?name .\n}'
correct = '"name" : {"type": "literal", "xml:lang" : "None", "value" : "Alice"}'

class Query(unittest.TestCase):

    def testQueryPlus(self):
        graph = ConjunctiveGraph()
        graph.parse(StringIO(test_data), format='n3')
        results = graph.query(test_query)
        self.failUnless(results.bindings[0]['name'] == 'Alice')


if __name__ == '__main__':
    unittest.main()