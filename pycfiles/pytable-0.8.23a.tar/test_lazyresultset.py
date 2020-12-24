# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/test_lazyresultset.py
# Compiled at: 2005-04-06 18:42:38
"""Tests of lazy result-set wrapper functionality"""
import unittest, traceback
from pytable import sqlquery, lazyresultset, specifierfromoptions
from pytable.tests import test_dbdriver
testSpec = specifierfromoptions.specifierFromOptions()

class LazyResultSetTests(unittest.TestCase):
    """Tests for the lazy result-set functionality"""
    __module__ = __name__
    (driver, connection) = testSpec.connect()

    def setUp(self):
        try:
            sqlquery.SQLQuery(sql='DROP TABLE LazyCursorTests;')(self.connection)
        except:
            self.connection.rollback()

        sqlquery.SQLQuery(sql='CREATE TABLE LazyCursorTests (\n\t\t\tfirst integer, second text\n\t\t);')(self.connection)
        sqlquery.SQLMultiQuery(sql='INSERT INTO LazyCursorTests( first,second)\n\t\t\tVALUES (%%(first)s, %%(second)s);')(self.connection, dataSet=[ {'first': a, 'second': str(a)} for a in range(1000) ])
        self.rawCursor = sqlquery.SQLQuery('SELECT * from LazyCursorTests ORDER BY first;')(self.connection)

    def testIteration(self):
        wrapped = lazyresultset.LazyResultSet(self.rawCursor)
        last = -1
        assert range(1000) == [ x[0] for x in wrapped ]

    def testRandomAccess(self):
        import random
        wrapped = lazyresultset.LazyResultSet(self.rawCursor)
        set = range(1000)
        random.shuffle(set)
        for item in set:
            assert wrapped[item][0] == item

    def testLength(self):
        wrapped = lazyresultset.LazyResultSet(self.rawCursor)
        assert len(wrapped) == 1000

    def testIndex(self):
        wrapped = lazyresultset.LazyResultSet(self.rawCursor)
        for index in range(0, 1000, 200):
            row = wrapped[index]
            assert wrapped.index(row) == row[0], 'Got wrong index for row %r' % (row,)
            assert row in wrapped, "Row doesn't show up in wrapped"

    def testRaises(self):
        wrapped = lazyresultset.LazyResultSet(self.rawCursor)
        self.failUnlessRaises(TypeError, wrapped.append, None)
        return

    def testSlice(self):
        wrapped = lazyresultset.LazyResultSet(self.rawCursor)
        other = range(1000)
        for (start, stop) in [(0, 50), (-300, 980), (400, 500)]:
            set = [ x[0] for x in wrapped[start:stop] ]
            assert set == other[start:stop], "Didn't get expected rows from slice\n%r\n%r" % (set, other[start:stop])

        set = [ x[0] for x in wrapped[20:50:2] ]
        assert set == range(20, 50, 2), "Extended slice didn't get expected rows"


if __name__ == '__main__':
    unittest.main()