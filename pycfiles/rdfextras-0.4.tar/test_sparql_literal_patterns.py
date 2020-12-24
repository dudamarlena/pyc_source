# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_literal_patterns.py
# Compiled at: 2012-02-24 05:27:21
from rdflib import ConjunctiveGraph
from rdflib import URIRef
from StringIO import StringIO
import rdflib
testRdf = '\n    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n    @prefix : <tag://example.org,2007/literals-test#> .\n\n    <http://example.org/thing>\n        :plain "plain";\n        :integer 1;\n        :float 1.1e0;\n        :decimal 1.1 ; \n        :string "string"^^xsd:string;\n        :date "2007-04-28"^^xsd:date;\n        :escape "a \\"test\\"";\n        rdfs:label "Thing"@en, "Sak"@sv .\n'
graph = ConjunctiveGraph()
graph.load(StringIO(testRdf), format='n3')
PROLOGUE = '\n    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n    PREFIX t: <tag://example.org,2007/literals-test#>\n'
thing = URIRef('http://example.org/thing')
SPARQL = PROLOGUE + ' SELECT ?uri WHERE { ?uri %s . } '
TEST_DATA = [
 (
  'plain', SPARQL % 't:plain "plain"', [(thing,)]),
 (
  'integer', SPARQL % 't:integer 1', [(thing,)]),
 (
  'decimal', SPARQL % 't:decimal 1.1', [(thing,)]),
 (
  'float', SPARQL % 't:float 1.1e0', [(thing,)]),
 (
  'langlabel_en', SPARQL % 'rdfs:label "Thing"@en', [(thing,)]),
 (
  'langlabel_sv', SPARQL % 'rdfs:label "Sak"@sv', [(thing,)]),
 (
  'string', SPARQL % 't:string "string"^^xsd:string', [(thing,)]),
 (
  'date', SPARQL % 't:date "2007-04-28"^^xsd:date', [(thing,)]),
 (
  'escape', SPARQL % 't:escape "a \\"test\\""', [(thing,)])]

def assert_equal(name, sparql, real, expected):
    assert real == expected, 'Failed test "%s":\n%s\n, expected\n\t%s\nand got\n\t%s\n' % (
     name, sparql, expected, real)


def test_generator():
    for name, sparql, expected in TEST_DATA:
        res = graph.query(sparql)
        yield (
         assert_equal, name, sparql, list(res), expected)


test_generator.sparql = True