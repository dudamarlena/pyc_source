# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_DAWG_DATASET_COMPLIANCE_flag.py
# Compiled at: 2012-04-24 09:28:08
import unittest
from nose.exc import SkipTest
from rdflib.graph import ConjunctiveGraph as Graph, URIRef
n3data = '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix : <http://goonmill.org/2007/skill.n3#> .\n\n:Foo a rdfs:Class .\n\n:bar a :Foo .'
ask_query = 'ASK { \n    <http://goonmill.org/2007/skill.n3#bar>         a         <http://goonmill.org/2007/skill.n3#Foo> \n}'
alicecontext = URIRef('http://example.org/foaf/aliceFoaf')
alicegraph = '# Named graph: http://example.org/foaf/aliceFoaf\n@prefix  foaf:     <http://xmlns.com/foaf/0.1/> .\n@prefix  rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix  rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .\n\n_:a  foaf:name     "Alice" .\n_:a  foaf:mbox     <mailto:alice@work.example> .\n_:a  foaf:knows    _:b .\n\n_:b  foaf:name     "Bob" .\n_:b  foaf:mbox     <mailto:bob@work.example> .\n_:b  foaf:nick     "Bobby" .\n_:b  rdfs:seeAlso  <http://example.org/foaf/bobFoaf> . \n<http://example.org/foaf/bobFoaf>\n     rdf:type      foaf:PersonalProfileDocument .\n'
bobcontext = URIRef('http://example.org/foaf/bobFoaf')
bobgraph = '# Named graph: http://example.org/foaf/bobFoaf\n@prefix  foaf:     <http://xmlns.com/foaf/0.1/> .\n@prefix  rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix  rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .\n\n_:z  foaf:mbox     <mailto:bob@work.example> .\n_:z  rdfs:seeAlso  <http://example.org/foaf/bobFoaf> .\n_:z  foaf:nick     "Robert" .\n\n<http://example.org/foaf/bobFoaf>\n     rdf:type      foaf:PersonalProfileDocument . '
alicebobselectquery = 'PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\nSELECT ?src ?bobNick\nFROM NAMED <http://example.org/foaf/aliceFoaf>\nFROM NAMED <http://example.org/foaf/bobFoaf>\nWHERE\n  {\n    GRAPH ?src\n    { ?x foaf:mbox <mailto:bob@work.example> .\n      ?x foaf:nick ?bobNick\n    }\n  }'
alicebobaskquery = 'PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\nASK \nFROM NAMED <http://example.org/foaf/aliceFoaf>\nFROM NAMED <http://example.org/foaf/bobFoaf>\n  {\n    ?x foaf:mbox <mailto:bob@work.example> .\n    ?x foaf:nick Robert .\n    }\n  }'
test4data = '@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n@prefix : <tag:example.org,2007;stuff/> .\n\n:a foaf:knows :b .\n:a foaf:knows :c .\n:a foaf:knows :d .\n\n:b foaf:knows :a .\n:b foaf:knows :c .\n\n:c foaf:knows :a .'
test4query = 'PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\nselect distinct ?person\nwhere {\n     ?person foaf:knows ?a .\n     ?person foaf:knows ?b .\n    filter (?a != ?b) .\n}'

class TestDAWG_DATASET_COMPLIANCE(unittest.TestCase):
    sparql = True

    def test1_ASK_when_DAWG_DATASET_COMPLIANCE_is_False(self):
        graph = Graph()
        graph.parse(data=n3data, format='n3')
        res = graph.query(ask_query)
        self.assert_(res.askAnswer == True, res.askAnswer)

    def test1_ASK_when_DAWG_DATASET_COMPLIANCE_is_True(self):
        raise SkipTest('known DAWG_DATATSET_COMPLIANCE SPARQL issue')
        graph = Graph()
        graph.parse(data=n3data, format='n3')
        res = graph.query(ask_query, dSCompliance=True)
        self.assert_(res.askAnswer == True, res.askAnswer)

    def test4_DAWG_DATASET_COMPLIANCE_is_False(self):
        graph = Graph()
        graph.parse(data=test4data, format='n3')
        res = graph.query(test4query)
        assert len(res) == 2

    def test4_DAWG_DATASET_COMPLIANCE_is_True(self):
        raise SkipTest('known DAWG_DATATSET_COMPLIANCE SPARQL issue')
        graph = Graph()
        graph.parse(data=test4data, format='n3')
        res = graph.query(test4query, dSCompliance=True)
        assert len(res) == 2