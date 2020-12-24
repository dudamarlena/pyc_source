# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_unit_tests.py
# Compiled at: 2012-02-24 05:27:21
from cStringIO import StringIO
from rdflib import URIRef
from rdflib.graph import Graph, ConjunctiveGraph
import rdflib
from rdflib.store import Store, NO_STORE
import unittest

class Option(object):

    def __init__(self):
        self.identifier = 'http://example.com'
        self.user = 'test'
        self.password = 'test'
        self.host = 'localhost'
        self.database = 'test'
        self.liveDB = False
        self.facts = False
        self.format = 'xml'


class AbstractSPARQLUnitTestCase(unittest.TestCase):
    """
    This is the base class for all unit tests in this module
    If TEST_FACTS is specified (as a class-level attribute), 
    then it is assumed to be a filesystem path to an RDF/XML 
    document that will be parsed and used as the set of facts 
    for the test case
    
    Note, an RDF graph is not required for tests that only exercise
    syntax alone (like the TestOPTVariableCorrelationTest below)
    """
    sparql = True
    debug = False
    TEST_FACT = None
    TEST_FACT_FORMAT = 'xml'

    def setUp(self):
        if singleGraph:
            self.graph = singleGraph
        else:
            self.graph = Graph(store)
        if self.TEST_FACT:
            print self.graph.store
            self.graph = Graph(self.graph.store)
            print 'Parsed %s facts for test (as %s)' % (
             len(self.graph.parse(self.TEST_FACT, format=self.TEST_FACT_FORMAT)),
             self.TEST_FACT_FORMAT)


BROKEN_OPTIONAL = '\nPREFIX ptrec: <tag:info@semanticdb.ccf.org,2007:PatientRecordTerms#>\nPREFIX ex: <http://example.org/>\nSELECT ?INTERVAL2\nWHERE {\n  ex:interval1 ptrec:hasDateTimeMax ?END1 .\n  OPTIONAL {\n    ?INTERVAL2 ptrec:hasDateTimeMax ?END2 .\n    FILTER (?END1 > ?END2)\n  }\n}'
BROKEN_OPTIONAL_DATA = ' \n@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n@prefix ptrec: <tag:info@semanticdb.ccf.org,2007:PatientRecordTerms#> .\n@prefix ex: <http://example.org/>.\n\nex:interval1 ptrec:hasDateTimeMax "2008-02-01"^^xsd:date .\nex:interval2 ptrec:hasDateTimeMax "2008-04-01"^^xsd:date .\nex:interval3 ptrec:hasDateTimeMax "2008-01-01"^^xsd:date .\n'

class TestOPTVariableCorrelationTest(AbstractSPARQLUnitTestCase):
    TEST_FACT = StringIO(BROKEN_OPTIONAL_DATA)
    TEST_FACT_FORMAT = 'n3'

    def test_OPT_FILTER(self):
        rt = list(self.graph.query(BROKEN_OPTIONAL, processor='sparql', DEBUG=self.debug))
        self.assertEqual(len(rt), 1)
        print ('rt[0]', rt[0])
        self.failUnless(rt[0][0] == URIRef('http://example.org/interval3'), 'ex:interval3 is the only other interval that preceded interval1')


UNIT_TESTS = [
 TestOPTVariableCorrelationTest]

class testSPARQLUnitTests(unittest.TestCase):
    global options
    global singleGraph
    global store
    store = 'IOMemory'
    options = Option()
    if options.facts and options.liveDB:
        op.error('options -l/--liveDB and -f/--facts are mutually exclusive!')
    from rdfextras.sparql import algebra
    algebra.DAWG_DATASET_COMPLIANCE = False
    store = rdflib.plugin.get('IOMemory', Store)(options.identifier)
    configurationString = ''
    rt = store.open(configurationString, create=False)
    if not options.liveDB:
        if rt == NO_STORE:
            store.open(configurationString, create=True)
        else:
            store.destroy(configurationString)
            store.open(configurationString, create=True)
    if options.facts:
        singleGraph = Graph().parse(options.facts, format=options.format)
    else:
        singleGraph = options.liveDB and ConjunctiveGraph(store) or None


UNIT_TESTS = [
 TestOPTVariableCorrelationTest]
if __name__ == '__main__':
    unittest.main()