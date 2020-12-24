# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_regex.py
# Compiled at: 2012-02-24 05:27:21
from rdflib import plugin
from rdflib.graph import ConjunctiveGraph
from rdflib.store import Store
from StringIO import StringIO
import unittest, rdflib
test_data = ' \n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n<http://example.org/bob>  foaf:name       "Bob" .\n<http://example.org/dave>  foaf:name       "Dave" .\n<http://example.org/alice>  foaf:name       "Alice" .\n<http://example.org/charlie>  foaf:name       "Charlie" .\n'
test_query = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\nSELECT ?name\nWHERE { ?x foaf:name ?name .\n        FILTER regex(?name, "a", "i") \n        }\n'

class TestRegex(unittest.TestCase):

    def testRegex(self):
        graph = ConjunctiveGraph(plugin.get('IOMemory', Store)())
        graph.parse(StringIO(test_data), format='n3')
        results = graph.query(test_query)
        self.failUnless(len([ a for a in results if 'a' in a[0] or 'A' in a[0] ]) == 3)


if __name__ == '__main__':
    unittest.main()