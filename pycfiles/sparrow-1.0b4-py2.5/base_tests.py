# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/tests/base_tests.py
# Compiled at: 2009-07-20 09:57:48
import os, StringIO
from unittest import TestCase, TestSuite, makeSuite, main
from sparrow.interfaces import ITripleStore, ISPARQLEndpoint
from sparrow.error import TripleStoreError, QueryError
TESTFILE = 'wine'
FORMATS = ['ntriples', 'rdfxml', 'turtle', 'json']

def open_test_file(format):
    extension = {'rdfxml': '.rdf', 'ntriples': '.nt', 
       'turtle': '.ttl', 
       'json': '.json'}
    filename = 'wine' + extension[format]
    return open(os.path.join(os.path.dirname(__file__), filename), 'r')


class TripleStoreTest(TestCase):

    def test_broken_parsing(self):
        self.assertRaises(TripleStoreError, self.db.add_rdfxml, '@', 'test', 'http://example.org')
        self.assertRaises(TripleStoreError, self.db.add_ntriples, '@', 'test')
        self.assertRaises(TripleStoreError, self.db.add_turtle, '@', 'test')
        self.assertRaises(TripleStoreError, self.db.add_json, '@', 'test')

    def test_rdfxml_parsing(self):
        self.db.add_rdfxml(open_test_file('rdfxml'), 'test', 'file://wine.rdf')
        triples = self.db.count('test') or self.db.count()
        if triples is not None:
            self.assertTrue(triples > 1500)
        return

    def test_ntriples_parsing(self):
        self.db.add_ntriples(open_test_file('ntriples'), 'test')
        triples = self.db.count('test') or self.db.count()
        if triples is not None:
            self.assertTrue(triples > 1500)
        return

    def test_turtle_parsing(self):
        self.db.add_turtle(open_test_file('turtle'), 'test')
        triples = self.db.count('test') or self.db.count()
        if triples is not None:
            self.assertTrue(triples > 1500)
        return

    def test_json_parsing(self):
        self.db.add_json(open_test_file('json'), 'test')
        triples = self.db.count('test') or self.db.count()
        if triples is not None:
            self.assertTrue(triples > 1500)
        return

    def test_base_uri_parsing(self):
        data = StringIO.StringIO('<?xml version="1.0"?>\n<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n <rdf:Description rdf:about="">\n  <foo:name xmlns:foo="http://foobar.com#">bar</foo:name>\n </rdf:Description>\n</rdf:RDF>')
        self.db.add_rdfxml(data, 'test', 'http://example.org')
        result = self.db.get_ntriples('test').read()
        self.assertEquals(result.strip()[:-1].strip(), '<http://example.org> <http://foobar.com#name> "bar"')

    def test_remove_statements(self):
        self.db.add_ntriples(open_test_file('ntriples'), 'test')
        fp = StringIO.StringIO('<http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine> <http://www.w3.org/2000/01/rdf-schema#label> "Wine Ontology" .\n')
        self.db.remove_ntriples(fp, 'test')
        data = self.db.get_ntriples('test').read()
        self.assertTrue('Wine Ontology' not in data)

    def test_ntriples_serializing(self):
        self.db.add_ntriples(open_test_file('ntriples'), 'test')
        data = self.db.get_ntriples('test').read()
        self.assertTrue('Wine Ontology' in data)

    def test_rdfxml_serializing(self):
        self.db.add_rdfxml(open_test_file('rdfxml'), 'test', 'file://wine.rdf')
        self.db.register_prefix('vin', 'http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#')
        data = self.db.get_rdfxml('test').read()
        self.assertTrue('Wine Ontology' in data)
        self.assertTrue('xmlns:vin' in data)

    def test_turtle_serializing(self):
        self.db.add_turtle(open_test_file('turtle'), 'test')
        self.db.register_prefix('vin', 'http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#')
        data = self.db.get_turtle('test').read()
        self.assertTrue('Wine Ontology' in data)
        self.assertTrue('@prefix vin' in data)

    def test_clear(self):
        count = self.db.count('test')
        if count is None:
            return
        self.assertEquals(count, 0)
        self.db.add_ntriples(open_test_file('ntriples'), 'test')
        count = self.db.count()
        self.assertTrue(count > 1500)
        self.db.clear('test')
        count = self.db.count()
        self.assertEquals(count, 0)
        return

    def test_contexts(self):
        self.assertEquals(list(self.db.contexts()), [])
        self.db.add_ntriples(open_test_file('ntriples'), 'a')
        self.db.add_ntriples(open_test_file('ntriples'), 'b')
        self.db.add_ntriples(open_test_file('ntriples'), 'c')
        self.assertEquals(sorted(list(self.db.contexts())), ['a', 'b', 'c'])
        self.db.clear('b')
        self.assertEquals(sorted(list(self.db.contexts())), ['a', 'c'])
        self.db.clear('a')
        self.db.clear('c')
        self.assertEquals(list(self.db.contexts()), [])


class TripleStoreQueryTest(TestCase):

    def test_ask(self):
        q = '\n        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>        \n        ASK { ?x rdfs:label "Wine Ontology"}\n        '
        self.assertTrue(self.db.ask(q))
        q = '\n        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>        \n        ASK { ?x rdfs:label "FooBar"}\n        '
        self.assertFalse(self.db.ask(q))

    def test_select(self):
        q = '\n        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n        prefix vin: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>\n        select ?grape\n        where { ?grape a vin:WineGrape .}\n        '
        result = self.db.select(q)
        self.assertEquals(len(result), 16)
        grapes = sorted([ r['grape']['value'].split('#')[(-1)] for r in result ])
        self.assertEquals(grapes, [
         'CabernetFrancGrape', 'CabernetSauvignonGrape',
         'ChardonnayGrape', 'CheninBlancGrape', 'GamayGrape',
         'MalbecGrape', 'MerlotGrape', 'PetiteSyrahGrape',
         'PetiteVerdotGrape', 'PinotBlancGrape', 'PinotNoirGrape',
         'RieslingGrape', 'SangioveseGrape', 'SauvignonBlancGrape',
         'SemillonGrape', 'ZinfandelGrape'])

    def test_select_literal_language(self):
        q = '\n        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n        PREFIX vin: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>\n        SELECT ?label\n        WHERE { vin:Wine rdfs:label ?label .}\n        '
        result = self.db.select(q)
        self.assertEquals(sorted(result), [
         {'label': {'type': 'literal', 'value': 'wine', 
                      'lang': 'en'}},
         {'label': {'type': 'literal', 'value': 'vin', 
                      'lang': 'fr'}}])

    def test_select_literal_datatype(self):
        q = '\n        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n        PREFIX vin: <http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine#>\n        SELECT ?year\n        WHERE { vin:Year1998 vin:yearValue ?year .}\n        '
        result = self.db.select(q)
        self.assertEquals(sorted(result), [
         {'year': {'type': 'literal', 
                     'value': '1998', 
                     'datatype': 'http://www.w3.org/2001/XMLSchema#positiveInteger'}}])

    def test_construct(self):
        q = '\n        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>        \n        CONSTRUCT {?x rdfs:label "Wine Ontology"}\n        WHERE { ?x rdfs:label "Wine Ontology" .}\n        '
        fp = self.db.construct(q, 'ntriples')
        self.assertEquals(fp.read().strip()[:-1].strip(), '<http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine> <http://www.w3.org/2000/01/rdf-schema#label> "Wine Ontology"')
        fp.close()

    def test_construct_dict(self):
        q = '\n        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>        \n        CONSTRUCT {?x rdfs:label "Wine Ontology"}\n        WHERE { ?x rdfs:label "Wine Ontology" .}\n        '
        data = self.db.construct(q, 'dict')
        self.assertEquals(data, {'http://www.w3.org/TR/2003/PR-owl-guide-20031209/wine': {'http://www.w3.org/2000/01/rdf-schema#label': [{'type': 'literal', 'value': 'Wine Ontology'}]}})

    def test_broken_query(self):
        self.assertRaises(QueryError, self.db.select, 'foo')
        self.assertRaises(QueryError, self.db.ask, 'foo')
        self.assertRaises(QueryError, self.db.construct, 'foo', 'rdfxml')