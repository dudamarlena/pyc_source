# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/test_namespaces.py
# Compiled at: 2012-10-25 06:18:24
"""
Unittests for namespace management.
"""
from django.utils import unittest
from rdflib.graph import Graph
from rdflib.term import URIRef
from rdflib_django.store import DjangoStore
XML_NAMESPACE = (
 'xml', URIRef('http://www.w3.org/XML/1998/namespace'))
RDF_NAMESPACE = ('rdf', URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
RDFS_NAMESPACE = ('rdfs', URIRef('http://www.w3.org/2000/01/rdf-schema#'))

class NamespaceTest(unittest.TestCase):
    """
    Tests for the weird behavior of RDFlib graphs and the default
    namespaces.
    """

    def setUp(self):
        self.store = DjangoStore()

    def testDefaultNamespaces(self):
        """
        Test the presence of the default namespaces.
        """
        g = Graph(store=self.store)
        namespaces = list(g.namespaces())
        self.assertIn(XML_NAMESPACE, namespaces)
        self.assertIn(RDF_NAMESPACE, namespaces)
        self.assertIn(RDFS_NAMESPACE, namespaces)
        g = Graph(store=self.store)
        g_namespaces = list(g.namespaces())
        self.assertIn(XML_NAMESPACE, g_namespaces)
        self.assertIn(RDF_NAMESPACE, g_namespaces)
        self.assertIn(RDFS_NAMESPACE, g_namespaces)

    def testCannotUpdateDefaultNamespaces(self):
        """
        Binding the prefix OR the URI of a default namespaces is a no-op.
        """
        g = Graph(store=self.store)
        self.assertIn(XML_NAMESPACE, list(g.namespaces()))
        g.bind('hello-world', XML_NAMESPACE[1])
        self.assertIn(XML_NAMESPACE, list(g.namespaces()))
        g.bind(XML_NAMESPACE, URIRef('http://example.com/xml'))
        self.assertIn(XML_NAMESPACE, list(g.namespaces()))

    def testBindingNamespaces(self):
        """
        Binding custom namespaces just works.
        """
        g = Graph(store=self.store)
        ns = ('prefix', URIRef('http://example.com/prefix'))
        self.assertNotIn(ns, list(g.namespaces()))
        g.bind(ns[0], ns[1])
        self.assertIn(ns, list(g.namespaces()))