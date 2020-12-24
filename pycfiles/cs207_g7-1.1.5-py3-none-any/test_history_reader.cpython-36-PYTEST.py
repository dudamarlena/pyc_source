# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/test/test_history_reader.py
# Compiled at: 2017-12-11 01:07:57
# Size of source mod 2**32: 2794 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest, pymysql
from kinetics.history import HistoryReader

class test_Reaction_History(unittest.TestCase):

    def test_connection(self):
        hr = HistoryReader()
        self.assertTrue(hr.db.open)

    def test_query_history_1(self):
        hr = HistoryReader()
        queryDict = {'species':None,  'temp':None,  'type':None}
        queryDict['temp'] = {'T':1600, 
         'cmp':'<'}
        result1, result2 = hr.queryDatabase(queryDict)
        self.assertFalse(result1 is None)
        self.assertFalse(result2 is None)

    def test_query_history_2(self):
        hr = HistoryReader()
        queryDict = {'species':None,  'temp':None,  'type':None}
        queryDict['species'] = ['H', 'O']
        queryDict['temp'] = {'T':1600,  'cmp':'<'}
        queryDict['type'] = 'non_reversible'
        result1, result2 = hr.queryDatabase(queryDict)
        self.assertFalse(result1 is None)
        self.assertFalse(result2 is None)

    def test_query_history_3(self):
        hr = HistoryReader()
        queryDict = {'species':None,  'temp':None,  'type':None}
        queryDict['species'] = 'OH'
        result1, result2 = hr.queryDatabase(queryDict)
        self.assertFalse(result1 is None)
        self.assertFalse(result2 is None)

    def test_database_tables(self):
        hr = HistoryReader()
        cursor = hr.getCursor()
        cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE="BASE TABLE" AND TABLE_SCHEMA ="cs207reactions"')
        tableNames = cursor.fetchall()
        self.assertEqual(str(tableNames), "(('reaction',), ('reaction_set',))")

    def test_close_connection(self):
        hr = HistoryReader()
        hr.db.close()
        cursor = hr.getCursor()
        cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE="BASE TABLE" AND TABLE_SCHEMA ="cs207reactions"')
        tableNames = cursor.fetchall()
        self.assertEqual(str(tableNames), "(('reaction',), ('reaction_set',))")