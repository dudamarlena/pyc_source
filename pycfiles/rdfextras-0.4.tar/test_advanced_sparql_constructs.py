# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_advanced_sparql_constructs.py
# Compiled at: 2012-04-24 09:28:08
import unittest
from rdflib import plugin
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib.term import URIRef
from rdflib.store import Store
from cStringIO import StringIO
from rdflib import Graph
import rdflib
try:
    set
except NameError:
    from sets import Set as set

testGraph1N3 = '\n@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix : <http://test/> .\n:foo :relatedTo [ a rdfs:Class ];\n     :parentOf ( [ a rdfs:Class ] ).\n:bar :relatedTo [ a rdfs:Resource ];\n     :parentOf ( [ a rdfs:Resource ] ).\n     \n( [ a rdfs:Resource ] ) :childOf :bar.     \n( [ a rdfs:Class ] )    :childOf :foo.\n'
sparqlQ1 = '\nBASE <http://test/>\nPREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?node WHERE { ?node :relatedTo [ a rdfs:Class ] }'
sparqlQ2 = '\nBASE <http://test/>\nPREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?node WHERE { ?node :parentOf ( [ a rdfs:Class ] ) }'
sparqlQ3 = '\nBASE <http://test/>\nPREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?node WHERE { ( [ a rdfs:Resource ] ) :childOf ?node }'
sparqlQ4 = '\nPREFIX owl:  <http://www.w3.org/2002/07/owl#> \n\nSELECT DISTINCT ?class \nFROM <http://www.w3.org/2002/07/owl#>\nWHERE { ?thing a ?class }'

class AdvancedTests(unittest.TestCase):

    def setUp(self):
        memStore = plugin.get('IOMemory', Store)()
        self.testGraph = Graph(memStore)
        self.testGraph.parse(StringIO(testGraph1N3), format='n3')

    def testNamedGraph(self):
        OWL_NS = Namespace('http://www.w3.org/2002/07/owl#')
        rt = self.testGraph.query(sparqlQ4)
        self.assertEquals(set(rt), set((x,) for x in [OWL_NS.DatatypeProperty, OWL_NS.ObjectProperty, OWL_NS.OntologyProperty, OWL_NS.Class, OWL_NS.Ontology, OWL_NS.AnnotationProperty, RDF.Property, RDFS.Class]))

    def testScopedBNodes(self):
        rt = self.testGraph.query(sparqlQ1)
        self.assertEquals(list(rt)[0][0], URIRef('http://test/foo'))

    def testCollectionContentWithinAndWithout(self):
        rt = self.testGraph.query(sparqlQ3)
        self.assertEquals(list(rt)[0][0], URIRef('http://test/bar'))

    def testCollectionAsObject(self):
        rt = self.testGraph.query(sparqlQ2)
        self.assertEquals(list(rt)[0][0], URIRef('http://test/foo'))
        self.assertEquals(1, len(rt))


if __name__ == '__main__':
    suite = unittest.makeSuite(AdvancedTests)
    unittest.TextTestRunner(verbosity=3).run(suite)