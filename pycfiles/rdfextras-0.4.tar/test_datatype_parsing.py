# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_datatype_parsing.py
# Compiled at: 2012-02-24 05:27:21
import unittest
from StringIO import StringIO
from rdflib.graph import ConjunctiveGraph
from rdflib.term import Literal
from rdflib.namespace import Namespace, XSD
testContent = '\n@prefix    :        <http://example.org/things#> .\n@prefix xsd:        <http://www.w3.org/2001/XMLSchema#> .\n:xi2 :p  "1"^^xsd:integer .\n:xd3 :p  "1"^^xsd:double .\n'
exNS = Namespace('http://example.org/things#')
double1 = Literal('1', datatype=XSD.double)

class TestSparqlOPT_FILTER(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.load(StringIO(testContent), format='n3')

    def test_OPT_FILTER(self):
        xd3Objs = [ o for o in self.graph.objects(subject=exNS.xd3, predicate=exNS.p)
                  ]
        self.failUnless(xd3Objs[0].datatype == XSD.double, 'Expecting %r, got instead : %r' % (double1, xd3Objs[0]))


if __name__ == '__main__':
    unittest.main()