# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdf/tests/test_graph.py
# Compiled at: 2008-03-16 19:10:10
import unittest
from rdf.graph import Graph
from rdf.term import URIRef, BNode, Literal, Namespace, RDF
from rdf.serializer import Serializer
from rdf import plugin

class GraphTestCase(unittest.TestCase):

    def setUp(self):
        self.g = Graph()

    def testLen(self):
        self.assertEquals(len(self.g), 0)

    def testHash(self):
        self.assertNotEquals(hash(self.g), 0)

    def testFinalNewline(self):
        """
        http://code.google.com/p/rdflib/issues/detail?id=5
        """
        failed = set()
        for p in plugin.plugins(None, Serializer):
            v = self.g.serialize(format=p.name)
            lines = v.split('\n')
            if '\n' not in v or lines[(-1)] != '':
                failed.add(p.name)

        self.assertEqual(len(failed), 0, "No final newline for formats: '%s'" % failed)
        return


if __name__ == '__main__':
    unittest.main()