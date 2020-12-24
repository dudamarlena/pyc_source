# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_advanced.py
# Compiled at: 2012-02-24 05:27:21
import doctest
from rdflib.namespace import RDF, RDFS, Namespace
from rdflib.term import Variable
from rdflib.graph import Graph
from cStringIO import StringIO
import rdflib
testData = '\n@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix : <http://test/> .\n:foo :relatedTo [ a rdfs:Class ];\n     :parentOf ( [ a rdfs:Class ] ).\n:bar :relatedTo [ a rdfs:Resource ];\n     :parentOf ( [ a rdfs:Resource ] ).\n     \n( [ a rdfs:Resource ] ) :childOf :bar.     \n( [ a rdfs:Class ] )    :childOf :foo.\n'
testData2 = '\n@prefix  foaf:  <http://xmlns.com/foaf/0.1/> .\n\n_:a    foaf:name   "Alice" .\n_:a    foaf:mbox   <mailto:alice@example.org> .\n'
testGraph = Graph().parse(StringIO(testData2), format='n3')
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
VCARD = Namespace('http://www.w3.org/2001/vcard-rdf/3.0#')

def describeOverride(terms, bindings, graph):
    g = Graph()
    for term in terms:
        if isinstance(term, Variable) and term not in bindings:
            continue
        else:
            term = bindings.get(term, term)
        for s, p, o in graph.triples((term, FOAF.mbox, None)):
            g.add((s, p, o))

    return g


namespaces = {'rdfs': RDF, 'rdf': RDFS, 
   'foaf': FOAF, 
   'vcard': VCARD, 
   'ex': Namespace('http://example.org/person#')}
for prefix, uri in namespaces.items():
    testGraph.namespace_manager.bind(prefix, uri, override=False)

if __name__ == '__main__':
    doctest.testfile('test_sparql_advanced.txt', globs=globals(), optionflags=doctest.ELLIPSIS)