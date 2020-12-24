# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_filter_bound.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.term import Literal, BNode, URIRef
from rdflib.graph import ConjunctiveGraph
from rdflib.namespace import Namespace
DC = Namespace('http://purl.org/dc/elements/1.1/')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
graph = ConjunctiveGraph()
s = BNode()
graph.add((s, FOAF['givenName'], Literal('Alice')))
b = BNode()
graph.add((b, FOAF['givenName'], Literal('Bob')))
graph.add((b, DC['date'], Literal('2005-04-04T04:04:04Z')))

def test_bound():
    res = list(graph.query('PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    PREFIX dc:  <http://purl.org/dc/elements/1.1/>\n    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>\n    SELECT ?name\n    WHERE { ?x foaf:givenName  ?name .\n                    OPTIONAL { ?x dc:date ?date } .\n                    FILTER ( bound(?date) ) }'))
    expected = [(Literal('Bob', lang=None, datatype=None),)]
    assert res == expected, 'Expected %s but got %s' % (expected, res)
    return


if __name__ == '__main__':
    test_bound()