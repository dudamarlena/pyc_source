# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/test_seq.py
# Compiled at: 2012-10-25 06:18:24
"""
Taken from https://github.com/RDFLib/rdflib/blob/master/test/test_seq.py
"""
import unittest
from rdflib.term import URIRef
from rdflib.graph import Graph
from rdflib_django.store import DjangoStore

class SeqTest(unittest.TestCase):
    """
    Tests sequences.
    """

    def setUp(self):
        store = self.store = Graph(store=DjangoStore())
        store.open(None)
        store.parse(data=s)
        return

    def tearDown(self):
        self.store.close()

    def testSeq(self):
        """
        Tests sequences.
        """
        items = self.store.seq(URIRef('http://example.org/Seq'))
        self.assertEquals(len(items), 6)
        self.assertEquals(items[(-1)].concrete(), URIRef('http://example.org/six'))
        self.assertEquals(items[2].concrete(), URIRef('http://example.org/three'))
        self.store.serialize()


s = '<?xml version="1.0" encoding="UTF-8"?>\n<rdf:RDF\n xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n xmlns="http://purl.org/rss/1.0/"\n xmlns:nzgls="http://www.nzgls.govt.nz/standard/"\n>\n <rdf:Seq rdf:about="http://example.org/Seq">\n   <rdf:li rdf:resource="http://example.org/one" />\n   <rdf:li rdf:resource="http://example.org/two" />\n   <rdf:li rdf:resource="http://example.org/three" />\n   <rdf:li rdf:resource="http://example.org/four" />\n   <rdf:li rdf:resource="http://example.org/five_five" />\n   <rdf:li rdf:resource="http://example.org/six" />\n </rdf:Seq>\n</rdf:RDF>\n'