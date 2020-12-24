# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_issue_10.py
# Compiled at: 2012-02-24 05:27:21
import unittest
from StringIO import StringIO
from rdflib.graph import ConjunctiveGraph
import rdflib
testgraph1 = '<rdf:RDF  xmlns:ex="http://temp.example.org/terms/"\n    xmlns:loc="http://simile.mit.edu/2005/05/ontologies/location#"\n    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">\n    \n   <ex:Event rdf:about="http://temp.example.org/terms/Event#case0">\n      <ex:date rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2007-12-31</ex:date>\n      <loc:place rdf:resource="http://temp.example.org/terms/Place#case1_place" />\n   </ex:Event>\n   <ex:Event rdf:about="http://temp.example.org/terms/Event#case1">\n      <ex:date rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-06</ex:date>\n      <loc:place rdf:resource="http://temp.example.org/terms/Place#case1_place" />\n   </ex:Event>\n   <ex:Event rdf:about="http://temp.example.org/terms/Event#case2">\n      <ex:starts rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-04</ex:starts>\n      <ex:finishes rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-05</ex:finishes>\n      <loc:place rdf:resource="http://temp.example.org/terms/Place#case2_place" />\n   </ex:Event>\n   <ex:Event rdf:about="http://temp.example.org/terms/Event#case3">\n      <ex:starts rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-07</ex:starts>\n      <ex:finishes rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-08</ex:finishes>\n      <loc:place rdf:resource="http://temp.example.org/terms/Place#case4_place" />\n   </ex:Event>\n   <ex:Event rdf:about="http://temp.example.org/terms/Event#case4">\n      <ex:starts rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-02</ex:starts>\n      <ex:finishes rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-03</ex:finishes>\n      <loc:place rdf:resource="http://temp.example.org/terms/Place#case3_place" />\n   </ex:Event>\n</rdf:RDF>'
testgraph2 = '<rdf:RDF  xmlns:ex="http://temp.example.org/terms/"\n    xmlns:loc="http://simile.mit.edu/2005/05/ontologies/location#"\n    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">\n    \n   <ex:Event rdf:about="http://temp.example.org/terms/Event#case5">\n      <ex:starts rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-09</ex:starts>\n      <ex:finishes rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-10</ex:finishes>\n      <loc:place rdf:resource="http://temp.example.org/terms/Place#case5_place" />\n   </ex:Event>\n   <ex:Event rdf:about="http://temp.example.org/terms/Event#case6">\n      <ex:starts rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-01</ex:starts>\n      <ex:finishes rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2008-01-11</ex:finishes>\n      <loc:place rdf:resource="http://temp.example.org/terms/Place#case6_place" />\n   </ex:Event>\n</rdf:RDF>'

class TestIssue10(unittest.TestCase):
    debug = False
    sparql = True

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.parse(StringIO(testgraph1), publicID='testgraph1')
        self.graph.parse(StringIO(testgraph2), publicID='testgraph2')

    def test_issue_10(self):
        res_var = self.graph.query('SELECT ?g ?s ?p ?o WHERE { GRAPH ?g { ?s ?p ?o } } ', processor='sparql', initNs={}, initBindings={}, DEBUG=False)
        res_star = self.graph.query('SELECT * WHERE { GRAPH ?g { ?s ?p ?o } } ', processor='sparql', initNs={}, initBindings={}, DEBUG=False)
        self.assertTrue(len(list(res_var)) == len(list(res_star)))