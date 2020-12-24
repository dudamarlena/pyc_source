# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_lang_tags.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from StringIO import StringIO
import unittest, rdflib
test_data = '\n@prefix : <http://ex.org> .\n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n:a  foaf:name "Alice" .\n:b  foaf:name "Alice"@no . \n:c  foaf:name "Alice"@fr-BE . \n\n'
test_query1 = 'PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nPREFIX : <http://ex.org>\nSELECT ?x\nWHERE {\n :a foaf:name ?x . \nFILTER (lang(?x)="")\n}'
test_query2 = 'PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nPREFIX : <http://ex.org>\nSELECT ?x\nWHERE {\n :b foaf:name ?x . \nFILTER (lang(?x)="no")\n}'
test_query3 = 'PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nPREFIX : <http://ex.org>\nSELECT ?x\nWHERE {\n :c foaf:name ?x . \nFILTER (langMatches(lang(?x),"FR"))\n}'
test_query4 = 'PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nPREFIX : <http://ex.org>\nSELECT ?x\nWHERE {\n :c foaf:name ?x . \nFILTER (langMatches(lang(?x),"*"))\n}'
test_query5 = 'PREFIX foaf:<http://xmlns.com/foaf/0.1/>\nPREFIX : <http://ex.org>\nSELECT ?x\nWHERE {\n :c foaf:name ?x . \nFILTER (langMatches(lang(?x),"NO"))\n}'
test_queries = [
 test_query1, test_query2, test_query3, test_query4]

class Query(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.parse(StringIO(test_data), format='n3')

    def test1(self):
        r = list(self.graph.query(test_query1))
        self.assertEqual(len(r), 1)

    def test2(self):
        r = list(self.graph.query(test_query2))
        self.assertEqual(len(r), 1)

    def test3(self):
        r = list(self.graph.query(test_query3))
        self.assertEqual(len(r), 1)

    def test4(self):
        r = list(self.graph.query(test_query4))
        self.assertEqual(len(r), 1)

    def test5(self):
        r = list(self.graph.query(test_query5))
        self.assertEqual(len(r), 0)


if __name__ == '__main__':
    unittest.main()