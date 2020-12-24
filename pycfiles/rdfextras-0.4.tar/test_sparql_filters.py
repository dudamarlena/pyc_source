# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_filters.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from rdflib.term import URIRef, Literal
from StringIO import StringIO
import rdflib
testContent = '\n    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n    <http://example.org/doc/1> rdfs:label "Document 1"@en, "Dokument 1"@sv .\n    <http://example.org/doc/2> rdfs:label "Document 2"@en, "Dokument 2"@sv .\n    <http://example.org/doc/3> rdfs:label "Document 3"@en, "Dokument 3"@sv .\n'
graph = ConjunctiveGraph()
graph.load(StringIO(testContent), format='n3')
doc1 = URIRef('http://example.org/doc/1')
PROLOGUE = '\n    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n'

def test_filter_by_lang():
    testdata = [
     ('en', '"Document 1"@en'),
     ('sv', '"Dokument 1"@sv')]
    query = PROLOGUE + '\n        SELECT ?label WHERE {\n            ' + doc1.n3() + ' rdfs:label ?label .\n            FILTER(LANG(?label) = "%s")\n        }\n    '
    for lang, literal in testdata:
        res = graph.query(query % lang)
        actual = [ binding[0].n3() for binding in res ]
        expected = [literal]
        yield (assert_equal, actual, expected)


def assert_equal(v1, v2):
    assert v1 == v2, 'Expected %r == %s' % (v1, v2)