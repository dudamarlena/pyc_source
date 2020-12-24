# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_equals.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef
from StringIO import StringIO
import unittest, rdflib

class TestSparqlEquals(unittest.TestCase):
    PREFIXES = {'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}

    def setUp(self):
        testContent = '\n            @prefix rdfs: <%(rdfs)s> .\n            <http://example.org/doc/1> rdfs:label "Document 1"@en .\n            <http://example.org/doc/2> rdfs:label "Document 2"@en .\n            <http://example.org/doc/3> rdfs:label "Document 3"@en .\n        ' % self.PREFIXES
        self.graph = ConjunctiveGraph()
        self.graph.load(StringIO(testContent), format='n3')

    def test_uri_equals(self):
        uri = URIRef('http://example.org/doc/1')
        query = ('\n            PREFIX rdfs: <%(rdfs)s>\n\n            SELECT ?uri WHERE {\n                ?uri rdfs:label ?label .\n                FILTER( ?uri = <' + uri + '> )\n            }\n        ') % self.PREFIXES
        res = self.graph.query(query)
        expected = [(uri,)]
        self.assertEqual(list(res), expected)


if __name__ == '__main__':
    unittest.main()