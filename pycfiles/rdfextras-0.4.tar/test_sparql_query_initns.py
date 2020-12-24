# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_query_initns.py
# Compiled at: 2012-04-24 09:28:08
import unittest
from rdflib import OWL, RDF, Graph, Namespace
import rdflib
xmldata = '<?xml version="1.0"?>\n<!DOCTYPE rdf:RDF [\n    <!ENTITY i "http://bug.rdflib/i.owl#" >\n    <!ENTITY owl "http://www.w3.org/2002/07/owl#" >\n    <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#" >\n    <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#" >\n    <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#" >\n]>\n<rdf:RDF xmlns="http://bug.rdflib/i.owl#"\n     xml:base="http://bug.rdflib/i.owl"\n     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n     xmlns:owl="http://www.w3.org/2002/07/owl#"\n     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"\n     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n     xmlns:i="http://bug.rdflib/i.owl#">\n    <owl:Ontology rdf:about="http://bug.rdflib/i.owl"/>\n    <owl:NamedIndividual rdf:about="&i;individual"/>\n</rdf:RDF>'
q = 'SELECT ?x\nWHERE {\n ?x rdf:type owl:NamedIndividual .\n}'
p = 'PREFIX owl: <http://www.w3.org/2002/07/owl#>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n'

def query(graph, querystring):
    processor = rdflib.plugin.get('sparql', rdflib.query.Processor)(graph)
    result = rdflib.plugin.get('sparql', rdflib.query.Result)
    ns = dict(graph.namespace_manager.namespaces())
    return result(processor.query(querystring, initNs=ns))


class TestSPARQLQueryinitNs(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.parse(data=xmldata)
        self.expect = set([ x for x, _, _ in self.graph.triples((
         None, RDF['type'], OWL['NamedIndividual']))
                          ])
        return

    def testnoprefix(self):
        ns = {'owl': Namespace('http://www.w3.org/2002/07/owl#'), 'rdf': Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')}
        got = set([ x for x, in self.graph.query(q, initNs=ns, DEBUG=True) ])
        assert self.expect == got, (self.expect, got)