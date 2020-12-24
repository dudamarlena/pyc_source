# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_parser_instability.py
# Compiled at: 2012-04-24 09:28:08
import unittest
from pyparsing import ParseException
BAD_SPARQL = '\nBASE <tag:chimezie@ogbuji.net,2007:exampleNS>.\nSELECT ?s\nWHERE { ?s ?p ?o }'

class TestBadSPARQL(unittest.TestCase):

    def test_bad_sparql(self):
        from rdflib import Graph
        g = Graph()
        self.assertRaises(ParseException, g.query, BAD_SPARQL)


if __name__ == '__main__':
    TestBadSPARQL.test_bad_sparql()