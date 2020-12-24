# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_misc.py
# Compiled at: 2012-02-24 05:27:21
import unittest, rdflib
from rdflib import term
import rdflib.compare
from rdflib.graph import Graph

class FakeBlankNode(object):

    def __cmp__(self, other):
        if other.__class__ == term.BNode:
            return True
        return False


blank_node = FakeBlankNode()

def create_graph(n3data):
    """
    :param n3data: data to create the graph from.
    :return: :class:`~rdflib.graph.Graph` instance containing parsed graph.
    """
    g = Graph()
    g.parse(data=n3data, format='n3')
    return g


class TestSimpleQueries(unittest.TestCase):
    """
    http://www.w3.org/TR/rdf-sparql-query/#basicpatterns
    """
    sparql = True

    def test_simple_query(self):
        """
        http://www.w3.org/TR/rdf-sparql-query/#WritingSimpleQueries
        """
        g = create_graph('\n<http://example.org/book/book1> <http://purl.org/dc/elements/1.1/title> "SPARQL Tutorial" .\n        ')
        results = g.query('\n        SELECT ?title\n        WHERE\n        {\n          <http://example.org/book/book1> <http://purl.org/dc/elements/1.1/title> ?title .\n        }\n        ')
        result_data = list(results)
        self.assertEqual(len(result_data), 1)
        self.assertEqual(len(result_data[0]), 1)
        self.assertEqual(result_data[0][0], 'SPARQL Tutorial')
        self.assertEqual(result_data[0][0].__class__, term.Literal)

    def test_multiple_matches(self):
        """
        http://www.w3.org/TR/rdf-sparql-query/#MultipleMatches
        """
        g = create_graph('\n        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .\n\n        _:a  foaf:name   "Johnny Lee Outlaw" .\n        _:a  foaf:mbox   <mailto:jlow@example.com> .\n        _:b  foaf:name   "Peter Goodguy" .\n        _:b  foaf:mbox   <mailto:peter@example.org> .\n        _:c  foaf:mbox   <mailto:carol@example.org> .\n        ')
        results = list(g.query('\n        PREFIX foaf:   <http://xmlns.com/foaf/0.1/>\n        SELECT ?name ?mbox\n        WHERE\n          { ?x foaf:name ?name .\n            ?x foaf:mbox ?mbox }\n        '))
        expected_results = [ (term.Literal(name), term.URIRef(mbox)) for name, mbox in [
         ('Johnny Lee Outlaw', 'mailto:jlow@example.com'),
         ('Peter Goodguy', 'mailto:peter@example.org')]
                           ]
        results.sort()
        expected_results.sort()
        self.assertEqual(results, expected_results)

    def test_blank_node_labels(self):
        """
        http://www.w3.org/TR/rdf-sparql-query/#BlankNodesInResults
        """
        g = create_graph('\n        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .\n\n        _:a  foaf:name   "Alice" .\n        _:b  foaf:name   "Bob" .\n        ')
        results = list(g.query('\n        PREFIX foaf:   <http://xmlns.com/foaf/0.1/>\n        SELECT ?x ?name\n        WHERE  { ?x foaf:name ?name }\n        '))
        col1, col2 = zip(*results)
        col1 = sorted(col1)
        col2 = sorted(col2)
        expected_results = sorted([
         term.Literal('Alice'),
         term.Literal('Bob')])
        self.assertEqual(col2, expected_results)
        self.assertNotEqual(col1[0], col1[1])
        self.assertEqual(col1[0].__class__, term.BNode)

    def test_construct(self):
        """
        http://www.w3.org/TR/rdf-sparql-query/#constructGraph
        """
        g = create_graph('\n        @prefix org:    <http://example.com/ns#> .\n\n        _:a  org:employeeName   "Alice" .\n        _:a  org:employeeId     12345 .\n\n        _:b  org:employeeName   "Bob" .\n        _:b  org:employeeId     67890 .\n        ')
        results = g.query('\n        PREFIX foaf:   <http://xmlns.com/foaf/0.1/>\n        PREFIX org:    <http://example.com/ns#>\n\n        CONSTRUCT { ?x foaf:name ?name }\n        WHERE  { ?x org:employeeName ?name }\n        ')
        expected_results = create_graph('\n        @prefix foaf: <http://xmlns.com/foaf/0.1/> .\n        @prefix org: <http://example.com/ns#> .\n              \n        _:x foaf:name "Alice" .\n        _:y foaf:name "Bob" .\n        ')
        self.assertEqual(rdflib.compare.to_isomorphic(results.graph), rdflib.compare.to_isomorphic(expected_results))


class TestRDFLiterals(unittest.TestCase):
    """
    http://www.w3.org/TR/rdf-sparql-query/#matchingRDFLiterals
    """
    sparql = True
    data = '\n        @prefix dt:   <http://example.org/datatype#> .\n        @prefix ns:   <http://example.org/ns#> .\n        @prefix :     <http://example.org/ns#> .\n        @prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .\n\n        :x   ns:p     "cat"@en .\n        :y   ns:p     "42"^^xsd:integer .\n        :z   ns:p     "abc"^^dt:specialDatatype .\n        '

    def test_match_language_tags(self):
        """
        http://www.w3.org/TR/rdf-sparql-query/#matchLangTags
        """
        g = create_graph(self.data)
        results = list(g.query('\n        SELECT ?v WHERE { ?v ?p "cat" }\n        '))
        expected_results = []
        self.assertEqual(results, expected_results)

    def test_match_literal_numeric_type(self):
        g = create_graph(self.data)
        results = list(g.query('\n        SELECT ?v WHERE { ?v ?p 42 }\n        '))
        expected_results = [(term.URIRef('http://example.org/ns#y'),)]
        self.assertEqual(results, expected_results)

    def test_match_literal_arbitary_type(self):
        g = create_graph(self.data)
        results = list(g.query('\n        SELECT ?v WHERE { ?v ?p "abc"^^<http://example.org/datatype#specialDatatype> }\n        '))
        expected_results = [(term.URIRef('http://example.org/ns#z'),)]
        self.assertEqual(results, expected_results)


class TestTermConstraints(unittest.TestCase):
    sparql = True
    data = '\n    @prefix dc:   <http://purl.org/dc/elements/1.1/> .\n    @prefix :     <http://example.org/book/> .\n    @prefix ns:   <http://example.org/ns#> .\n\n    :book1  dc:title  "SPARQL Tutorial" .\n    :book1  ns:price  42 .\n    :book2  dc:title  "The Semantic Web" .\n    :book2  ns:price  23 .\n    '

    def test_string_values(self):
        g = create_graph(self.data)
        results = sorted(g.query('\n        PREFIX  dc:  <http://purl.org/dc/elements/1.1/>\n        SELECT  ?title\n        WHERE   { ?x dc:title ?title\n                  FILTER regex(?title, "^SPARQL") \n                }\n        '))
        expected_results = [(term.Literal('SPARQL Tutorial'),)]
        self.assertEqual(results, expected_results)

    def test_case_insentitive(self):
        g = create_graph(self.data)
        results = sorted(g.query('\n        PREFIX  dc:  <http://purl.org/dc/elements/1.1/>\n        SELECT  ?title\n        WHERE   { ?x dc:title ?title\n                  FILTER regex(?title, "web", "i" ) \n                }\n        '))
        expected_results = [(term.Literal('The Semantic Web'),)]
        self.assertEqual(results, expected_results)

    def test_numeric_values(self):
        g = create_graph(self.data)
        results = sorted(g.query('\n        PREFIX  dc:  <http://purl.org/dc/elements/1.1/>\n        PREFIX  ns:  <http://example.org/ns#>\n        SELECT  ?title ?price\n        WHERE   { ?x ns:price ?price .\n                  FILTER (?price < 30.5)\n                  ?x dc:title ?title . }\n        '))
        expected_results = [(term.Literal('The Semantic Web'), term.Literal(23))]
        self.assertEqual(results, expected_results)


if __name__ == '__main__':
    unittest.main()