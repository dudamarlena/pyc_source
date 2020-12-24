# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_sparql_parser_nestedbrackets.py
# Compiled at: 2012-02-24 05:27:21
from rdfextras.sparql.parser import parse
query = '\nPREFIX foaf:    <http://xmlns.com/foaf/0.1/>\nSELECT ?name ?mbox\nWHERE  { { ?x foaf:name ?name . }\n         { ?x foaf:mbox ?mbox . }\n       }\n'
correct = "{ [<SPARQLParser.GraphPattern: [[?x [foaf:name([u'?name'])], ?x [foaf:mbox([u'?mbox'])]]]>] }"
if __name__ == '__main__':
    p = parse(query)
    tmp = p.query.whereClause.parsedGraphPattern
    if str(tmp) == correct:
        print 'PASSED'