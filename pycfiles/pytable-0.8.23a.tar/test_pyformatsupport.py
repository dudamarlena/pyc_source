# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/tests/test_pyformatsupport.py
# Compiled at: 2004-11-16 07:03:23
import unittest, traceback
from pytable import dbspecifier, dbschema, sqlquery, specifierfromoptions, pyformatsupport
testSpec = specifierfromoptions.specifierFromOptions()
primarySpecifiers = specifiers = [
 testSpec]

class PyFormatTest(unittest.TestCase):
    __module__ = __name__

    def testQmark1(self):
        """Does qmark support produce expected result"""
        query = 'SELECT * FROM x WHERE this = %(this)s\n\t\tAND that = %(that)s'
        values = {'this': 23, 'that': 24}
        pf = pyformatsupport.PyFormatSupport(values, 'qmark')
        newQuery = query % pf
        assert newQuery == 'SELECT * FROM x WHERE this = ?\n\t\tAND that = ?'
        assert len(pf.sequential) == 2
        assert pf.sequential == [23, 24]
        pf.finishBuilding()
        result = newQuery % pf
        assert len(pf.sequential) == 2

    def testQmark2(self):
        """Does support for multiple refs to same value"""
        query = 'SELECT * FROM x WHERE this = %(this)s\n\t\tAND that = %(this)s'
        values = {'this': 23, 'that': 24}
        pf = pyformatsupport.PyFormatSupport(values, 'qmark')
        newQuery = query % pf
        assert newQuery == 'SELECT * FROM x WHERE this = ?\n\t\tAND that = ?'
        assert len(pf.sequential) == 2
        assert pf.sequential == [23, 23]
        pf.finishBuilding()
        result = newQuery % pf
        assert len(pf.sequential) == 2

    def testFormat(self):
        """Does format support produce expected result"""
        query = 'SELECT * FROM x WHERE this = %(this)s\n\t\tAND that = %(that)s AND this2 = %(this)s'
        values = {'this': 23, 'that': 24}
        pf = pyformatsupport.PyFormatSupport(values, 'format')
        newQuery = query % pf
        assert newQuery == 'SELECT * FROM x WHERE this = %s\n\t\tAND that = %s AND this2 = %s', newQuery
        assert len(pf.sequential) == 3
        assert pf.sequential == [23, 24, 23]
        pf.finishBuilding()
        result = newQuery % tuple(pf)
        assert len(pf.sequential) == 3
        assert result == 'SELECT * FROM x WHERE this = 23\n\t\tAND that = 24 AND this2 = 23', result

    def testNumeric(self):
        """Does numeric support produce expected result"""
        query = 'SELECT * FROM x WHERE this = %(this)s\n\t\tAND that = %(that)s AND this2 = %(this)s'
        values = {'this': 23, 'that': 24}
        pf = pyformatsupport.PyFormatSupport(values, 'numeric')
        newQuery = query % pf
        assert newQuery == 'SELECT * FROM x WHERE this = :0\n\t\tAND that = :1 AND this2 = :2', newQuery
        assert len(pf.sequential) == 3
        assert pf.sequential == [23, 24, 23]
        pf.finishBuilding()
        result = newQuery % pf
        assert len(pf.sequential) == 3

    def testNamed(self):
        """Does named support produce expected result"""
        query = 'SELECT * FROM x WHERE this = %(this)s\n\t\tAND that = %(that)s AND this2 = %(this)s'
        values = {'this': 23, 'that': 24}
        pf = pyformatsupport.PyFormatSupport(values, 'named')
        newQuery = query % pf
        assert newQuery == 'SELECT * FROM x WHERE this = :this\n\t\tAND that = :that AND this2 = :this', newQuery
        assert len(pf.sequential) == 3
        assert pf.sequential == [23, 24, 23]
        pf.finishBuilding()
        result = newQuery % pf
        assert len(pf.sequential) == 3


if __name__ == '__main__':
    unittest.main()