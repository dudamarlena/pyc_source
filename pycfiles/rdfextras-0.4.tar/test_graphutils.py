# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_graphutils.py
# Compiled at: 2012-02-24 05:27:21
import unittest
try:
    from pydot import Dot
except ImportError:
    from nose import SkipTest
    raise SkipTest('pydot required but not installed')

from StringIO import StringIO
from rdfextras.utils import graphutils
from rdflib.graph import Graph
n3source = '@prefix : <http://www.w3.org/2000/10/swap/Primer#>.\n@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix owl:  <http://www.w3.org/2002/07/owl#> .\n@prefix dc:  <http://purl.org/dc/elements/1.1/> .\n@prefix foo: <http://www.w3.org/2000/10/swap/Primer#>.\n@prefix swap: <http://www.w3.org/2000/10/swap/>.\n\n<> dc:title\n  "Primer - Getting into the Semantic Web and RDF using N3".\n\n<#pat> <#knows> <#jo> .\n<#pat> <#age> 24 .\n<#al> is <#child> of <#pat> .\n\n<#pat> <#child>  <#al>, <#chaz>, <#mo> ;\n       <#age>    24 ;\n       <#eyecolor> "blue" .\n\n:Person a rdfs:Class.\n\n:Pat a :Person.\n\n:Woman a rdfs:Class; rdfs:subClassOf :Person .\n\n:sister a rdf:Property.\n\n:sister rdfs:domain :Person; \n        rdfs:range :Woman.\n\n:Woman = foo:FemaleAdult .\n:Title a rdf:Property; = dc:title .\n\n'

class TestUtilN3toDot(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.graph.parse(StringIO(n3source), format='n3')
        self.dot = Dot()

    def test_util_graph_to_dot(self):
        res = graphutils.graph_to_dot(self.graph, self.dot)
        res = self.dot.to_string()
        self.assert_('swap/Primer#Person' in res, res)


if __name__ == '__main__':
    unittest.main()