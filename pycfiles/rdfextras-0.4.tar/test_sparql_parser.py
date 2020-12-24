# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_parser.py
# Compiled at: 2012-04-24 09:28:08
import unittest
from rdflib import Graph

def buildQueryArgs(q):
    return dict(select='', where='', optional='')


class SPARQLParserTest(unittest.TestCase):
    known_issue = True

    def setUp(self):
        self.graph = Graph()

    def tearDown(self):
        pass


tests = [
 ('basic', '    SELECT ?name\n    WHERE { ?a <http://xmlns.com/foaf/0.1/name> ?name }'),
 ('simple_prefix', '    PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    SELECT ?name\n    WHERE { ?a foaf:name ?name }'),
 ('base_statement', '    BASE <http://xmlns.com/foaf/0.1/>\n    SELECT ?name\n    WHERE { ?a <name> ?name }'),
 ('prefix_and_colon_only_prefix', '    PREFIX : <http://xmlns.com/foaf/0.1/>\n    PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0#>\n    SELECT ?name ?title\n    WHERE {\n        ?a :name ?name .\n        ?a vcard:TITLE ?title\n    }'),
 ('predicate_object_list_notation', '    PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    SELECT ?name ?mbox\n    WHERE {\n        ?x  foaf:name  ?name ;\n            foaf:mbox  ?mbox .\n    }'),
 ('object_list_notation', '    PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    SELECT ?x\n    WHERE {\n        ?x foaf:nick  "Alice" ,\n                      "Alice_" .\n    }\n    '),
 ('escaped_literals', '    PREFIX tag: <http://xmlns.com/foaf/0.1/>\n    PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0#>\n    SELECT ?name\n    WHERE {\n        ?a tag:name ?name ;\n           vcard:TITLE "escape test vcard:TITLE " ;\n           <tag://test/escaping> "This is a \'\'\' Test """" ;\n           <tag://test/escaping> ?d\n    }\n    '),
 ('key_word_as_variable', '    PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    SELECT ?PREFIX ?WHERE\n    WHERE {\n        ?x  foaf:name  ?PREFIX ;\n            foaf:mbox  ?WHERE .\n    }'),
 ('key_word_as_prefix', '    PREFIX WHERE: <http://xmlns.com/foaf/0.1/>\n    SELECT ?name ?mbox\n    WHERE {\n        ?x  WHERE:name  ?name ;\n            WHERE:mbox  ?mbox .\n    }'),
 ('some_test_cases_from_grammar_py_1', '    SELECT ?title \n    WHERE { \n        <http://example.org/book/book1> \n        <http://purl.org/dc/elements/1.1/title> \n        ?title . \n    }'),
 ('some_test_cases_from_grammar_py_2', '    PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    SELECT ?name ?mbox\n    WHERE { ?person foaf:name ?name .\n    OPTIONAL { ?person foaf:mbox ?mbox}\n    }'),
 ('some_test_cases_from_grammar_py_3', '    PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    SELECT ?name ?name2\n    WHERE { ?person foaf:name ?name .\n    OPTIONAL { ?person foaf:knows ?p2 . ?p2 foaf:name   ?name2 . }\n    }'),
 ('some_test_cases_from_grammar_py_4', '    PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n    #PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n    SELECT ?name ?mbox\n    WHERE\n    {\n        { ?person rdf:type foaf:Person } .\n        OPTIONAL { ?person foaf:name  ?name } .\n        OPTIONAL {?person foaf:mbox  ?mbox} .\n    }')]

def _buildQueryArg(q):
    res = buildQueryArgs(q)
    assert res.get('select', False) and res['select'] is not None
    if res.get('where', False):
        assert res['where'] is not None
        assert res.get('optional', False) and res['optional'] is not None
    return