# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_issue_45.py
# Compiled at: 2012-02-24 05:27:21
import unittest
from rdflib.graph import ConjunctiveGraph as Graph
from rdfextras.sparql import algebra
from StringIO import StringIO
import rdflib

class TestSparqlASK(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        io = StringIO('\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix : <http://goonmill.org/2007/skill.n3#> .\n\n:Foo a rdfs:Class .\n\n:bar a :Foo .\n')
        self.graph.load(io, format='n3')
        self.compliance_setting, algebra.DAWG_DATASET_COMPLIANCE = algebra.DAWG_DATASET_COMPLIANCE, False

    def tearDown(self):
        algebra.DAWG_DATASET_COMPLIANCE = self.compliance_setting

    def test_ask_true(self):
        """
        Ask for a triple that exists, assert that the response is True.
        """
        res = self.graph.query('ASK { <http://goonmill.org/2007/skill.n3#bar> a <http://goonmill.org/2007/skill.n3#Foo> } ')
        self.assertEquals(res.askAnswer, True, 'The answer should have been that the triple was found')

    def test_ask_false(self):
        """
        Ask for a triple that does not exist, assert that the response is False.
        """
        res = self.graph.query('ASK { <http://goonmill.org/2007/skill.n3#baz> a <http://goonmill.org/2007/skill.n3#Foo> } ')
        self.assertEquals(res.askAnswer, False, 'The answer should have been that the triple was not found')


if __name__ == '__main__':
    unittest.main()