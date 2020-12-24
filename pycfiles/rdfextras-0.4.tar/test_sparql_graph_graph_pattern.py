# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_graph_graph_pattern.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef, Literal
from rdflib.namespace import RDFS
from StringIO import StringIO
import unittest
testContent = '\n@prefix foaf:  <http://xmlns.com/foaf/0.1/> .\n<http://purl.org/net/chimezie/foaf#chime> \n  foaf:name   "Chime";\n  a foaf:Person.\n<http://eikeon.com/> foaf:knows \n  <http://purl.org/net/chimezie/foaf#chime>,<http://www.ivan-herman.net/>.\n<http://www.ivan-herman.net/> foaf:name "Ivan".'
doc1 = URIRef('http://eikeon.com/')
QUERY = '\nPREFIX foaf:   <http://xmlns.com/foaf/0.1/>\nSELECT ?X\nWHERE { \n    ?P a foaf:Person .\n    ?X foaf:knows ?P .\n    OPTIONAL { \n      ?X foaf:knows ?OP .\n      ?OP foaf:name "Judas" } \n    FILTER (!bound(?OP)) }'

class TestSparqlOPT_FILTER2(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.load(StringIO(testContent), format='n3')

    def test_OPT_FILTER(self):
        results = self.graph.query(QUERY, DEBUG=False)
        results = list(results)
        self.failUnless(results == [(doc1,)], 'expecting : %s .  Got: %s' % ([(doc1,)], repr(results)))


if __name__ == '__main__':
    unittest.main()