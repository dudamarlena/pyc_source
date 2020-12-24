# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_issue_43.py
# Compiled at: 2012-07-13 08:11:28
import unittest
from rdflib import RDF
from rdflib.graph import ConjunctiveGraph
testgraph = '@prefix rdf: <%s> .\n<http://example.org/a> rdf:value "a" .' % RDF.uri
testquery = 'SELECT ?node1 ?val1\nWHERE {\n    ?node1 rdf:value ?val1 .\n    FILTER (\n        ?val1="never match0" || ?val1="never match1" && ?val1="never match2"\n    )\n}\n'
disjunctionquery = 'SELECT ?node1 ?val1\nWHERE {\n    ?node1 rdf:value ?val1 .\n    FILTER (?val1="never match" && ?val1="never match")\n}\n'
conjunctionquery = 'SELECT ?node1 ?val1\nWHERE {\n    ?node1 rdf:value ?val1 .\n    FILTER (?val1="never match" || ?val1="never match")\n}\n'

class TestIssue43(unittest.TestCase):
    debug = False
    sparql = True
    known_issue = True

    def setUp(self):
        NS = 'http://example.org/'
        self.graph = ConjunctiveGraph()
        self.graph.parse(data=testgraph, format='n3', publicID=NS)

    def testSPARQL_disjunction(self):
        rt = self.graph.query(disjunctionquery, initNs={'rdf': RDF}, DEBUG=False)
        self.assertEquals(len(list(rt)), 0)

    def testSPARQL_conjunction(self):
        rt = self.graph.query(conjunctionquery, initNs={'rdf': RDF}, DEBUG=False)
        self.assertEquals(len(list(rt)), 0)

    def testSPARQL_disjunction_with_conjunction(self):
        rt = self.graph.query(testquery, initNs={'rdf': RDF}, DEBUG=True)
        self.assertEquals(len(list(rt)), 0, list(rt))


if __name__ == '__main__':
    TestIssue43.testSPARQL_disjunction_with_conjunction()