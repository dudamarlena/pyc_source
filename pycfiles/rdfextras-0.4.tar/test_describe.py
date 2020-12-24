# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_describe.py
# Compiled at: 2012-04-24 09:28:08
import unittest, rdflib

class TestDescribe(unittest.TestCase):

    def test_simple_describe(self):
        g = rdflib.Graph()
        g.add((rdflib.URIRef('urn:a'),
         rdflib.URIRef('urn:b'),
         rdflib.URIRef('urn:c')))
        res = g.query('DESCRIBE <urn:a>', DEBUG=True)
        self.assertEqual(len(res), 1)

    def test_complex_describe(self):
        n3data = '        @prefix  foaf:  <http://xmlns.com/foaf/0.1/> .\n\n        _:a    foaf:name   "Alice" .\n        _:a    foaf:mbox   <mailto:alice@example.org> .'
        g = rdflib.Graph()
        g.parse(data=n3data, format='n3')
        describe_query = '        PREFIX foaf:   <http://xmlns.com/foaf/0.1/>\n        DESCRIBE ?x\n        WHERE    { ?x foaf:mbox <mailto:alice@example.org> } '
        res = g.query(describe_query, DEBUG=True)
        res = (
         ('').join([ r[0] for r in res ])[1:-1],)
        self.assertEqual(len(res), 1)


if __name__ == '__main__':
    unittest.main()