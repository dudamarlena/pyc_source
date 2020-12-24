# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_filter_extensions.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from rdflib.namespace import Namespace, RDF, XSD
from rdflib.term import BNode, Literal
import rdflib
DC = Namespace('http://purl.org/dc/elements/1.1/')
FUNC = Namespace('http://example.org/functions#')
graph = ConjunctiveGraph()
graph.add((BNode(), RDF.value, Literal(0)))
graph.add((BNode(), RDF.value, Literal(1)))
graph.add((BNode(), RDF.value, Literal(2)))
graph.add((BNode(), RDF.value, Literal(3)))
from rdflib.term import _toPythonMapping
NUMERIC_TYPES = [ type_uri for type_uri in _toPythonMapping if _toPythonMapping[type_uri] in (int, float, long)
                ]

def func_even(a):
    from rdfextras.sparql.sparqlOperators import getValue
    value = getValue(a)
    if isinstance(value, Literal) and value.datatype in NUMERIC_TYPES:
        return Literal(int(value.toPython() % 2 == 0), datatype=XSD.boolean)
    raise TypeError(a)


def test_even_extension():
    res = list(graph.query('\n    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n    PREFIX func:  <http://example.org/functions#>\n\n    SELECT ?value\n    WHERE { ?x rdf:value ?value . FILTER ( func:even(?value) ) }\n\n    '))
    res.sort()
    expected = [(Literal(0),), (Literal(2),)]
    assert res == expected, 'Expected %s but got %s' % (expected, res)


test_even_extension.sparql = True
test_even_extension.known_issue = True
if __name__ == '__main__':
    test_even_extension()