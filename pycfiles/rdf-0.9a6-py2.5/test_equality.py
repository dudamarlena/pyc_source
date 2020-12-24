# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdf/tests/test_equality.py
# Compiled at: 2008-03-16 19:10:10
import unittest
from rdf.term import URIRef, BNode, Literal, RDF
from rdf.graph import Graph
CORE_SYNTAX_TERMS = [
 RDF['RDF'], RDF['ID'], RDF['about'], RDF['parseType'],
 RDF['resource'], RDF['nodeID'], RDF['datatype']]

class IdentifierEquality(unittest.TestCase):

    def setUp(self):
        self.uriref = URIRef('http://example.org/')
        self.bnode = BNode()
        self.literal = Literal('http://example.org/')
        self.python_literal = 'http://example.org/'
        self.python_literal_2 = 'foo'

    def testA(self):
        self.assertEquals(self.uriref == self.literal, False)

    def testB(self):
        self.assertEquals(self.literal == self.uriref, False)

    def testC(self):
        self.assertEquals(self.uriref == self.python_literal, False)

    def testD(self):
        self.assertEquals(self.python_literal == self.uriref, False)

    def testE(self):
        self.assertEquals(self.literal == self.python_literal, False)

    def testF(self):
        self.assertEquals(self.python_literal == self.literal, False)

    def testG(self):
        self.assertEquals('foo' in CORE_SYNTAX_TERMS, False)

    def testH(self):
        self.assertEquals(URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#RDF') in CORE_SYNTAX_TERMS, True)

    def testI(self):
        g = Graph()
        g.add((self.uriref, RDF['value'], self.literal))
        g.add((self.uriref, RDF['value'], self.uriref))
        self.assertEqual(len(g), 2)


if __name__ == '__main__':
    unittest.main()