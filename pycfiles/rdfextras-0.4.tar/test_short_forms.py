# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_short_forms.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.namespace import RDF, RDFS
from rdflib.store import Store
from rdflib import plugin
from rdflib.parser import StringInputSource
from rdflib.graph import Graph
from rdflib.py3compat import b
import unittest, sys, rdflib
problematic_query = '\nBASE <http://www.clevelandclinic.org/heartcenter/ontologies/DataNodes.owl#>\nPREFIX dnode: <http://www.clevelandclinic.org/heartcenter/ontologies/DataNodes.owl#>\nPREFIX owl: <http://www.w3.org/2000/07/owl#>\nPREFIX ptrec: <tag:info@semanticdb.ccf.org,2007:PatientRecordTerms#>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX sts: <tag:info@semanticdb.ccf.org,2008:STS.2.61#>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nSELECT ?VAR0 ?VAR1 ?VAR2 ?VAR3\nWHERE {\n  ?VAR0 <tag:info@semanticdb.ccf.org,2007:PatientRecordTerms#hasCardiacValveEtiology> <tag:info@semanticdb.ccf.org,2007:PatientRecordTerms#CardiacValveEtiology_thrombosis> .\n  ?VAR0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <tag:info@semanticdb.ccf.org,2007:PatientRecordTerms#SurgicalProcedure_cardiac_valve_mitral_valve_repair> .\n  ?VAR1 <http://www.clevelandclinic.org/heartcenter/ontologies/DataNodes.owl#contains> ?VAR0 .\n  ?VAR2 <http://www.clevelandclinic.org/heartcenter/ontologies/DataNodes.owl#contains> ?VAR1 .\n  ?VAR2 <http://www.clevelandclinic.org/heartcenter/ontologies/DataNodes.owl#contains> ?VAR3 .\n  ?VAR3 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <tag:info@semanticdb.ccf.org,2007:PatientRecordTerms#Patient> .\n} \n'

class TestSPARQLAbbreviations(unittest.TestCase):
    sparql = True

    def setUp(self):
        global store
        NS = 'http://example.org/'
        self.graph = Graph(store)
        self.graph.parse(StringInputSource(b('\n           @prefix    : <http://example.org/> .\n           @prefix rdf: <%s> .\n           @prefix rdfs: <%s> .\n           [ :prop :val ].\n           [ a rdfs:Class ].' % (RDF, RDFS))), format='n3')

    def testTypeAbbreviation(self):
        global debug
        query = 'SELECT ?subj WHERE { ?subj a rdfs:Class }'
        print query
        rt = self.graph.query(query, DEBUG=debug)
        self.failUnless(len(rt) == 1, 'Should be a single match: %s' % len(rt))
        query = 'SELECT ?subj WHERE { ?subj a <http://www.w3.org/2000/01/rdf-schema#Class> }'
        print query
        rt = self.graph.query(query, DEBUG=debug)
        self.failUnless(len(rt) == 1, 'Should be a single match: %s' % len(rt))

    def testTypeAbbreviation(self):
        query = 'SELECT ?subj WHERE { ?subj a rdfs:Class }'
        print query
        rt = self.graph.query(query, DEBUG=debug)
        self.failUnless(len(rt) == 1, 'Should be a single match: %s' % len(rt))
        query = 'SELECT ?subj WHERE { ?subj a <http://www.w3.org/2000/01/rdf-schema#Class> }'
        print query
        rt = self.graph.query(query, DEBUG=debug)
        self.failUnless(len(rt) == 1, 'Should be a single match: %s' % len(rt))

    def testQNameVSFull(self):
        query = 'SELECT ?subj WHERE { ?subj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> rdfs:Class }'
        print query
        rt = self.graph.query(query, DEBUG=debug)
        self.failUnless(len(rt) == 1, 'Should be a single matchL: %s' % len(rt))
        query = 'SELECT ?subj WHERE { ?subj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }'
        print query
        rt = self.graph.query(query, DEBUG=debug)
        self.failUnless(len(rt) == 1, 'Should be a single match: %s' % len(rt))

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
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSPARQLAbbreviations)
    unittest.TextTestRunner(verbosity=2).run(suite)