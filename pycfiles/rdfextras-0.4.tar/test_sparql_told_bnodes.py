# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_told_bnodes.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.term import Variable
from rdflib.namespace import RDF, RDFS
from rdflib.store import Store
from rdflib import plugin
from rdflib.parser import StringInputSource
from rdflib import Graph
import unittest, sys, rdflib

class TestSPARQLToldBNodes(unittest.TestCase):
    known_issue = True
    sparql = True

    def setUp(self):
        global store
        NS = 'http://example.org/'
        self.graph = Graph(store)
        self.graph.parse(StringInputSource('\n           @prefix    : <http://example.org/> .\n           @prefix rdf: <%s> .\n           @prefix rdfs: <%s> .\n           [ :prop :val ].\n           [ a rdfs:Class ].' % (RDF, RDFS)), format='n3')

    def testToldBNode(self):
        global debug
        for s, p, o in self.graph.triples((None, RDF.type, None)):
            pass

        query = 'SELECT ?obj WHERE { %s ?prop ?obj }' % s.n3()
        print query
        rt = self.graph.query(query, DEBUG=debug)
        print list(rt)
        self.failUnless(len(rt) == 1, "BGP should only match the 'told' BNode by name (result set size: %s)" % len(rt))
        bindings = {Variable('subj'): s}
        query = 'SELECT ?obj WHERE { ?subj ?prop ?obj }'
        print query
        rt = self.graph.query(query, initBindings=bindings, DEBUG=debug)
        self.failUnless(len(rt) == 1, "BGP should only match the 'told' BNode by name (result set size: %s, BNode: %s)" % (len(rt), s.n3()))
        return

    def testFilterBNode(self):
        for s, p, o in self.graph.triples((None, RDF.type, None)):
            pass

        query2 = 'SELECT ?subj WHERE { ?subj ?prop ?obj FILTER( ?subj != %s ) }' % s.n3()
        print query2
        rt = self.graph.query(query2, DEBUG=True)
        self.failUnless(len(rt) == 1, "FILTER should exclude 'told' BNodes by name (result set size: %s, BNode excluded: %s)" % (len(rt), s.n3()))
        return

    def tearDown(self):
        self.graph.store.rollback()


store = 'IOMemory'
debug = False
if __name__ == '__main__':
    from optparse import OptionParser
    usage = 'usage: %prog [options]'
    op = OptionParser(usage=usage)
    op.add_option('-s', '--storeKind', default='IOMemory', help='The (class) name of the store to use for persistence')
    op.add_option('-c', '--config', default='', help='Configuration string to use for connecting to persistence store')
    op.add_option('-i', '--identifier', default='', help='Store identifier')
    op.add_option('-d', '--debug', action='store_true', default=False, help='Debug flag')
    options, args = op.parse_args()
    debug = options.debug
    store = plugin.get(options.storeKind, Store)(options.identifier)
    store.open(options.config, create=False)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSPARQLToldBNodes)
    unittest.TextTestRunner(verbosity=2).run(suite)