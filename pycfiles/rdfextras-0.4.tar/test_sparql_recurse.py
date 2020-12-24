# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_recurse.py
# Compiled at: 2012-02-24 05:27:21
from rdflib import ConjunctiveGraph, URIRef, Literal
from StringIO import StringIO
import unittest, nose, rdflib
testContent = '\n@prefix foaf:  <http://xmlns.com/foaf/0.1/> .\n@prefix dc: <http://purl.org/dc/elements/1.1/>.\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n<http://del.icio.us/rss/chimezie/logic> \n  a foaf:Document;\n  dc:date "2006-10-01T12:35:00"^^xsd:dateTime.\n<http://del.icio.us/rss/chimezie/paper> \n  a foaf:Document;\n  dc:date "2005-05-25T08:15:00"^^xsd:dateTime.\n<http://del.icio.us/rss/chimezie/illustration> \n  a foaf:Document;\n  dc:date "1990-01-01T12:45:00"^^xsd:dateTime.'
BASIC_KNOWS_DATA = '\n@prefix foaf:  <http://xmlns.com/foaf/0.1/> .\n\n<ex:person.1> foaf:name "person 1";\n              foaf:knows <ex:person.2>.\n<ex:person.2> foaf:knows <ex:person.3>.\n<ex:person.3> foaf:name "person 3".\n'
KNOWS_QUERY = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\nSELECT ?x ?name\n{\n  ?x foaf:knows ?y .\n  OPTIONAL { ?y foaf:name ?name }\n}\nRECUR ?y TO ?x\n'
SUBCLASS_DATA = '\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n<ex:ob> a <ex:class.1> .\n<ex:class.1> rdfs:subClassOf <ex:class.2> .\n<ex:class.2> rdfs:subClassOf <ex:class.3> .\n'
SUBCLASS_QUERY = '\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nSELECT ?x ?t \n{ ?x rdf:type ?t }\nRECUR ?t TO ?x\n{ ?x rdfs:subClassOf ?t }\n'
ANSWER1 = URIRef('http://del.icio.us/rss/chimezie/paper')

class RecursionTests(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.load(StringIO(testContent), format='n3')

    def test_simple_recursion(self):
        graph = ConjunctiveGraph()
        graph.load(StringIO(BASIC_KNOWS_DATA), format='n3')
        results = graph.query(KNOWS_QUERY, processor='sparql', DEBUG=False)
        results = set(results)
        person1 = URIRef('ex:person.1')
        person2 = URIRef('ex:person.2')
        nose.tools.assert_equal(results, set([(person1, None), (person1, Literal('person 3')),
         (
          person2, Literal('person 3'))]))
        return

    def test_secondary_recursion(self):
        graph = ConjunctiveGraph()
        graph.load(StringIO(SUBCLASS_DATA), format='n3')
        results = graph.query(SUBCLASS_QUERY, processor='sparql', DEBUG=False)
        results = set(results)
        ob = URIRef('ex:ob')
        class1 = URIRef('ex:class.1')
        class2 = URIRef('ex:class.2')
        class3 = URIRef('ex:class.3')
        nose.tools.assert_equal(results, set([(ob, class1), (ob, class2), (ob, class3)]))


if __name__ == '__main__':
    unittest.main()