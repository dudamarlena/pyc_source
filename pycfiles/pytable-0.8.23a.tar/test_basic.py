# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/test_basic.py
# Compiled at: 2005-04-06 18:42:38
import unittest, sys
from pytable import dbspecifier, sqlquery, specifierfromoptions
getAll = sqlquery.SQLQuery(queryString='SELECT * from temp')
testSpec = specifierfromoptions.specifierFromOptions()
validSpec = {'driver': 'pypgsql', 'user': 'mike', 'password': 'pass', 'host': 'localhost', 'database': 'test'}

class SpecTest(unittest.TestCase):
    __module__ = __name__

    def testSpecCreate(self):
        return dbspecifier.DBSpecifier(**validSpec)

    def testSpecJoin(self):
        result = self.testSpecCreate() + dbspecifier.DBSpecifier(password='past', host='localhost', database='test', dsn='that')
        assert result.password == 'past', "Didn't update password on join"
        assert result.dsn == 'that', "Didn't update dsn on join"
        return result

    def testSpecCmp(self):
        assert cmp(self.testSpecCreate(), self.testSpecJoin()) == -1, "Comparison didn't get proper order"


class ConnectionTests(unittest.TestCase):
    """Test ability to connect"""
    __module__ = __name__

    def test_simpleConnect(self):
        """Connect to each of the specifiers in local_specifiers module"""
        testSpec.connect()

    def test_connectCache(self):
        (d1, a) = testSpec.connect()
        b = d1.connect(testSpec)
        assert a is b, "Connection cache doesn't return the same connection for same spec: %s" % (spec,)


if __name__ == '__main__':
    unittest.main()