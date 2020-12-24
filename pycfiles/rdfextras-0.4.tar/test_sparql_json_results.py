# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_json_results.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.graph import ConjunctiveGraph
from StringIO import StringIO
import unittest, rdflib
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise ImportError('unable to find json or simplejson modules')

test_data = '\n@prefix foaf:       <http://xmlns.com/foaf/0.1/> .\n@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n<http://example.org/alice> a foaf:Person;\n    foaf:name "Alice";\n    foaf:knows <http://example.org/bob> .\n\n<http://example.org/bob> a foaf:Person;\n    foaf:name "Bob" .\n'
PROLOGUE = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\n'
test_material = {}
test_material['optional'] = (
 PROLOGUE + '\n    SELECT ?name ?x ?friend\n    WHERE { ?x foaf:name ?name .\n            OPTIONAL { ?x foaf:knows ?friend . }\n    }\n    ', {'head': {'vars': ['name', 'x', 'friend']}, 'results': {'bindings': [{'x': {'type': 'uri', 'value': 'http://example.org/alice'}, 'name': {'type': 'literal', 'value': 'Alice'}, 'friend': {'type': 'uri', 'value': 'http://example.org/bob'}}, {'x': {'type': 'uri', 'value': 'http://example.org/bob'}, 'name': {'type': 'literal', 'value': 'Bob'}}]}})
test_material['select_vars'] = (
 PROLOGUE + '\n    SELECT ?name ?friend\n    WHERE { ?x foaf:name ?name .\n            OPTIONAL { ?x foaf:knows ?friend . }\n    }', {'head': {'vars': ['name', 'friend']}, 'results': {'bindings': [{'name': {'type': 'literal', 'value': 'Bob'}}, {'name': {'type': 'literal', 'value': 'Alice'}, 'friend': {'type': 'uri', 'value': 'http://example.org/bob'}}]}})
test_material['wildcard'] = (
 PROLOGUE + '\n    SELECT * WHERE { ?x foaf:name ?name . }\n    ', {'head': {'vars': ['x', 'name']}, 'results': {'bindings': [{'x': {'type': 'uri', 'value': 'http://example.org/bob'}, 'name': {'type': 'literal', 'value': 'Bob'}}, {'x': {'type': 'uri', 'value': 'http://example.org/alice'}, 'name': {'type': 'literal', 'value': 'Alice'}}]}})
test_material['wildcard_vars'] = (
 PROLOGUE + '\n    SELECT * WHERE { ?x foaf:name ?name . }\n    ', {'head': {'vars': ['x', 'name']}, 'results': {'bindings': [{'x': {'type': 'uri', 'value': 'http://example.org/alice'}, 'name': {'type': 'literal', 'value': 'Alice'}}, {'x': {'type': 'uri', 'value': 'http://example.org/bob'}, 'name': {'type': 'literal', 'value': 'Bob'}}]}})
test_material['union'] = (
 PROLOGUE + '\n    SELECT DISTINCT ?name WHERE {\n                { <http://example.org/alice> foaf:name ?name . } UNION { <http://example.org/bob> foaf:name ?name . }\n    }\n    ', {'head': {'vars': ['name']}, 'results': {'bindings': [{'name': {'type': 'literal', 'value': 'Bob'}}, {'name': {'type': 'literal', 'value': 'Alice'}}]}})
test_material['union3'] = (
 PROLOGUE + '\n    SELECT DISTINCT ?name WHERE {\n                { <http://example.org/alice> foaf:name ?name . }\n                UNION { <http://example.org/bob> foaf:name ?name . }\n                UNION { <http://example.org/nobody> foaf:name ?name . }\n    }\n            ', {'head': {'vars': ['name']}, 'results': {'bindings': [{'name': {'type': 'literal', 'value': 'Bob'}}, {'name': {'type': 'literal', 'value': 'Alice'}}]}})

def make_method(testname):

    def test(self):
        query, correct = test_material[testname]
        self._query_result_contains(query, correct)

    test.__name__ = 'test%s' % testname.title()
    return test


class TestSparqlJsonResults(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.parse(StringIO(test_data), format='n3')

    def _query_result_contains(self, query, correct):
        results = self.graph.query(query)
        result_json = json.loads(results.serialize(format='json').decode('utf-8'))
        msg = 'Expected:\n %s \n- to contain:\n%s' % (result_json, correct)
        self.assertEqual(result_json['head'], correct['head'], msg)
        result_bindings = sorted(result_json['results']['bindings'], key=repr)
        correct_bindings = sorted(correct['results']['bindings'], key=repr)
        msg = 'Expected:\n %s \n- to contain:\n%s' % (result_bindings, correct_bindings)
        self.failUnless(result_bindings == correct_bindings, msg)

    testOptional = make_method('optional')
    testWildcard = make_method('wildcard')
    testUnion = make_method('union')
    testUnion3 = make_method('union3')
    testSelectVars = make_method('select_vars')
    testWildcardVars = make_method('wildcard_vars')


if __name__ == '__main__':
    unittest.main()