# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_base_ref.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from rdflib.term import Literal
from StringIO import StringIO
import unittest, rdflib
test_data = '\n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n<http://example.org/alice> a foaf:Person;\n    foaf:name "Alice";\n    foaf:knows <http://example.org/bob> .'
test_query = '\nBASE <http://xmlns.com/foaf/0.1/>\nSELECT ?name\nWHERE { [ a :Person ; :name ?name ] }'

class TestSparqlJsonResults(unittest.TestCase):
    sparql = True

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.parse(StringIO(test_data), format='n3')

    def test_base_ref(self):
        rt = list(self.graph.query(test_query))
        self.failUnless(rt[0][0] == Literal('Alice'), "Expected:\n 'Alice' \nGot:\n %s" % rt)


if __name__ == '__main__':
    unittest.main()