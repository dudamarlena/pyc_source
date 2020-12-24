# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_date_filter.py
# Compiled at: 2012-02-24 05:27:21
from rdflib import ConjunctiveGraph, URIRef
from nose.exc import SkipTest
from StringIO import StringIO
import unittest, rdflib
testContent = '\n@prefix foaf:  <http://xmlns.com/foaf/0.1/> .\n@prefix dc: <http://purl.org/dc/elements/1.1/>.\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n<http://del.icio.us/rss/chimezie/logic> \n  a foaf:Document;\n  dc:date "2006-10-01T12:35:00"^^xsd:dateTime.\n<http://del.icio.us/rss/chimezie/paper> \n  a foaf:Document;\n  dc:date "2005-05-25T08:15:00"^^xsd:dateTime.\n<http://del.icio.us/rss/chimezie/illustration> \n  a foaf:Document;\n  dc:date "1990-01-01T12:45:00"^^xsd:dateTime.'
QUERY1 = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\nPREFIX   dc: <http://purl.org/dc/elements/1.1/>\nPREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>\nSELECT ?doc\nWHERE { \n  ?doc a foaf:Document;\n       dc:date ?date. \n    FILTER (?date < xsd:dateTime("2006-01-01T00:00:00") && \n            ?date > xsd:dateTime("1995-06-15T00:00:00")) }'
QUERY2 = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\nPREFIX   dc: <http://purl.org/dc/elements/1.1/>\nPREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>\nSELECT ?doc\nWHERE { \n  ?doc a foaf:Document;\n       dc:date ?date. \n    FILTER (?date < "2006-01-01T00:00:00" && \n            ?date > "1995-06-15T00:00:00") }'
QUERY3 = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\nPREFIX   dc: <http://purl.org/dc/elements/1.1/>\nPREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>\nSELECT ?doc\nWHERE { \n  ?doc a foaf:Document;\n       dc:date ?date. \n    FILTER (?date < "2006-01-01T00:00:00"^^xsd:dateTime && \n            ?date > "1995-06-15T00:00:00"^^xsd:dateTime ) }'
ANSWER1 = URIRef('http://del.icio.us/rss/chimezie/paper')

class DateFilterTest(unittest.TestCase):

    def setUp(self):
        self.graph = ConjunctiveGraph()
        self.graph.load(StringIO(testContent), format='n3')

    def test_DATE_FILTER1(self):
        for query in [QUERY1, QUERY2, QUERY3]:
            if query == QUERY1 and rdflib.py3compat.PY3:
                raise SkipTest('Known issue with Python 3')
            results = self.graph.query(query, processor='sparql', DEBUG=False)
            results = list(results)
            self.failUnless(len(results) and results == [(ANSWER1,)], 'expecting : %s .  Got: %s' % ([(ANSWER1,)], repr(results)))


if __name__ == '__main__':
    unittest.main()