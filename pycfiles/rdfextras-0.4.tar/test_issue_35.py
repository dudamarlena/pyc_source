# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_sparql/test_issue_35.py
# Compiled at: 2012-02-24 05:27:21
import unittest
from rdfextras.sparql.parser import Query
qstring = 'SELECT ?f where { ?f <#b> <c#d> }'

class TestIssue35(unittest.TestCase):

    def test_issue_35(self):
        res = Query.parseString(qstring)
        assert res is not None
        return


if __name__ == '__main__':
    unittest.main()