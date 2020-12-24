# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_xml_results.py
# Compiled at: 2012-02-24 05:27:21
import sys
from nose.exc import SkipTest
if sys.platform.startswith('java'):
    raise SkipTest('Skipped failing test in Jython')
if sys.version_info[:2] < (2, 6):
    raise SkipTest('Skipped, known XML namespace issue with Python < 2.6')
from rdflib.graph import ConjunctiveGraph
from rdflib.py3compat import b
import re, unittest
test_data = '\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n<http://example.org/word>\n    rdfs:label "Word"@en;\n    rdf:value 1;\n    rdfs:seeAlso [] .\n\n'
PROLOGUE = '\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX owl:  <http://www.w3.org/2002/07/owl#>\n'
query = PROLOGUE + '\nSELECT ?s ?o WHERE { ?s ?p ?o . }\n'
expected_fragments = [
 b('</sparql:head><sparql:results>'),
 b('<sparql:binding name="s"><sparql:uri>http://example.org/word</sparql:uri></sparql:binding>'),
 b('<sparql:binding name="o"><sparql:bnode>'),
 b('<sparql:binding name="o"><sparql:literal datatype="http://www.w3.org/2001/XMLSchema#integer">1</sparql:literal></sparql:binding>'),
 b('<sparql:result><sparql:binding name="s"><sparql:uri>http://example.org/word</sparql:uri></sparql:binding><sparql:binding name="o"><sparql:literal xml:lang="en">Word</sparql:literal></sparql:binding></sparql:result>')]

class TestSparqlXmlResults(unittest.TestCase):
    sparql = True

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.parse(data=test_data, format='n3')

    def testSimple(self):
        self._query_result_contains(query, expected_fragments)

    def _query_result_contains(self, query, fragments):
        results = self.graph.query(query)
        result_xml = results.serialize(format='xml')
        result_xml = normalize(result_xml)
        for frag in fragments:
            self.failUnless(frag in result_xml)


def normalize(s, exp=re.compile(b('\\s+'), re.MULTILINE)):
    return exp.sub(b(' '), s)


if __name__ == '__main__':
    unittest.main()