# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_naf.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef
from rdflib.namespace import RDFS
from StringIO import StringIO
import unittest, rdflib
testContent = '\n    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n    <http://example.org/doc/1> rdfs:label "Document 1","Document 2".\n    <http://example.org/doc/2> rdfs:label "Document 1".'
doc1 = URIRef('http://example.org/doc/1')
doc2 = URIRef('http://example.org/doc/2')
QUERY = '\nSELECT ?X\nWHERE { \n    ?X ?label "Document 1".\n    OPTIONAL { ?X ?label ?otherLabel.  FILTER ( ?otherLabel != "Document 1" ) } \n    FILTER (!bound(?otherLabel)) }'

class TestSparqlOPT_FILTER(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.load(StringIO(testContent), format='n3')

    def test_OPT_FILTER(self):
        results = self.graph.query(QUERY, DEBUG=False, initBindings={'?label': RDFS.label})
        print results.vars
        self.failUnless(list(results) == [(doc2,)], 'expecting : %s, got %s' % (repr([(doc2,)]), repr(list(results))))


if __name__ == '__main__':
    unittest.main()