# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_leaves.py
# Compiled at: 2012-02-24 05:27:21
import doctest
data = '\n@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n@prefix : <tag:example.org,2007;stuff/> .\n\n:a foaf:knows :b .\n:a foaf:knows :c .\n:a foaf:knows :d .\n\n:b foaf:knows :a .\n:b foaf:knows :c .\n\n:c foaf:knows :a .\n\n'
query = '\nPREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\nselect distinct ?person\nwhere {\n    ?person foaf:knows ?a .\n    ?person foaf:knows ?b .\n   filter (?a != ?b) .\n}\n'

def test_leaves():
    return doctest.DocFileSuite('leaves.txt')


if __name__ == '__main__':
    doctest.testfile('leaves.txt', globs=globals(), optionflags=doctest.ELLIPSIS)