# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_results.py
# Compiled at: 2012-07-18 09:06:05
import sys
from nose.exc import SkipTest
import unittest, rdflib
from StringIO import StringIO

class TestSparqlResultsFormats(unittest.TestCase):

    def _test(self, s, format):
        r = rdflib.query.Result.parse(StringIO(s), format=format)
        print r.type
        s = r.serialize(format=format)
        r2 = rdflib.query.Result.parse(StringIO(s.decode('utf-8')), format=format)
        self.assertEqual(r, r2)

    def testXML(self):
        if sys.version_info[:2] < (2, 6):
            raise SkipTest('Skipped, known issue with XML namespaces under Python < 2.6')
        xmlres = '<?xml version="1.0"?>\n<sparql xmlns="http://www.w3.org/2005/sparql-results#"\n        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n        xsi:schemaLocation="http://www.w3.org/2001/sw/DataAccess/rf1/result2.xsd">\n\n  <head>\n    <variable name="x"/>\n    <variable name="hpage"/>\n    <variable name="name"/>\n    <variable name="mbox"/>\n    <variable name="age"/>\n    <variable name="blurb"/>\n    <variable name="friend"/>\n\n    <link href="example.rq" />\n  </head>\n\n  <results>\n\n    <result>\n      <binding name="x"><bnode>r1</bnode></binding>\n      <binding name="hpage"><uri>http://work.example.org/alice/</uri></binding>\n      <binding name="name"><literal>Alice</literal></binding>\n      <binding name="mbox"><literal></literal></binding>\n      <binding name="friend"><bnode>r2</bnode></binding>\n      <binding name="blurb"><literal datatype="http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral">&lt;p xmlns="http://www.w3.org/1999/xhtml"&gt;My name is &lt;b&gt;alice&lt;/b&gt;&lt;/p&gt;</literal></binding>\n    </result>\n\n    <result> \n      <binding name="x"><bnode>r2</bnode></binding>\n      <binding name="hpage"><uri>http://work.example.org/bob/</uri></binding>\n      <binding name="name"><literal xml:lang="en">Bob</literal></binding>\n      <binding name="mbox"><uri>mailto:bob@work.example.org</uri></binding>\n      <binding name="age"><literal datatype="http://www.w3.org/2001/XMLSchema#integer">30</literal></binding>\n      <binding name="friend"><bnode>r1</bnode></binding>\n    </result>\n\n  </results>\n\n</sparql>\n'
        self._test(xmlres, 'xml')

    def testjson(self):
        jsonres = '{\n   "head": {\n       "link": [\n           "http://www.w3.org/TR/rdf-sparql-XMLres/example.rq"\n           ],\n       "vars": [\n           "x",\n           "hpage",\n           "name",\n           "mbox",\n           "age",\n           "blurb",\n           "friend"\n           ]\n       },\n   "results": {\n       "bindings": [\n               {\n                   "x" : {\n                     "type": "bnode",\n                     "value": "r1"\n                   },\n\n                   "hpage" : {\n                     "type": "uri",\n                     "value": "http://work.example.org/alice/"\n                   },\n\n                   "name" : {\n                     "type": "literal",\n                     "value": "Alice"\n                   },\n                   \n                   "mbox" : {\n                     "type": "literal",\n                     "value": ""\n                   },\n\n                   "blurb" : {\n                     "datatype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral",\n                     "type": "typed-literal",\n                     "value": "<p xmlns=\\"http://www.w3.org/1999/xhtml\\">My name is <b>alice</b></p>"\n                   },\n\n                   "friend" : {\n                     "type": "bnode",\n                     "value": "r2"\n                   }\n               },{\n                   "x" : {\n                     "type": "bnode",\n                     "value": "r2"\n                   },\n                   \n                   "hpage" : {\n                     "type": "uri",\n                     "value": "http://work.example.org/bob/"\n                   },\n                   \n                   "name" : {\n                     "type": "literal",\n                     "value": "Bob",\n                     "xml:lang": "en"\n                   },\n\n                   "mbox" : {\n                     "type": "uri",\n                     "value": "mailto:bob@work.example.org"\n                   },\n\n                   "friend" : {\n                     "type": "bnode",\n                     "value": "r1"\n                   }\n               }\n           ]\n       }\n   }\n'
        self._test(jsonres, 'json')


if __name__ == '__main__':
    unittest.main()