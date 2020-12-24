# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_issue_11.py
# Compiled at: 2012-04-24 09:28:08
import unittest
from rdflib import RDF
from rdflib.graph import ConjunctiveGraph
testgraph = '@prefix    : <http://example.org/> .\n@prefix rdf: <%s> .\n:foo rdf:value 1 .\n:bar rdf:value -2 .' % RDF.uri
testquery = 'SELECT ?node \nWHERE {\n    ?node rdf:value ?val .\n    FILTER (?val < -1) \n}'

class TestIssue11(unittest.TestCase):
    debug = False
    sparql = True

    def setUp(self):
        NS = 'http://example.org/'
        self.graph = ConjunctiveGraph()
        self.graph.parse(data=testgraph, format='n3', publicID=NS)

    def testSPARQL_lessthan_filter_using_negative_integer(self):
        rt = self.graph.query(testquery, initNs={'rdf': RDF}, DEBUG=True)
        for row in rt:
            assert str(row[0]) == 'http://example.org/bar'


if __name__ == '__main__':
    TestIssue11.testSPARQL_lessthan_filter_using_negative_integer()