# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_sqltype.py
# Compiled at: 2019-04-15 16:23:56
# Size of source mod 2**32: 3892 bytes
import unittest
from py_db_wrapper import sqlType
from py_db_wrapper import dialect
from py_db_wrapper import exceptions

class TestSqlTypeMethods(unittest.TestCase):

    def test_sql_string_size(self):
        sql_type = sqlType.STRING()
        self.assertEqual('varchar', sql_type.sql_string(dialect.Mssql))

    def test_sql_string_size(self):
        sql_type = sqlType.STRING(size=1)
        self.assertEqual('varchar(1)', sql_type.sql_string(dialect.Mssql))

    def test_sql_string_size_1(self):
        sql_type = sqlType.STRING(size='max')
        self.assertEqual('varchar(max)', sql_type.sql_string(dialect.Mssql))

    def test_sql_string_double_size(self):
        sql_type = sqlType.DECIMAL(size='1,2')
        self.assertEqual('decimal(1,2)', sql_type.sql_string(dialect.Mssql))

    def test_convert_type_string(self):
        conversions = {dialect.Mysql: [
                         {'input_value':'BIGINT', 
                          'expected_value':'bigint',  'convert_to_dialect':dialect.Mssql},
                         {'input_value':'TINYINT', 
                          'expected_value':'tinyint',  'convert_to_dialect':dialect.Mssql},
                         {'input_value':'INT', 
                          'expected_value':'int',  'convert_to_dialect':dialect.Mssql},
                         {'input_value':'BIGINT', 
                          'expected_value':'BIGINT',  'convert_to_dialect':dialect.Hive},
                         {'input_value':'TINYINT', 
                          'expected_value':'TINYINT',  'convert_to_dialect':dialect.Hive},
                         {'input_value':'INT', 
                          'expected_value':'INT',  'convert_to_dialect':dialect.Hive}], 
         
         dialect.Mssql: [
                         {'input_value':'bigint', 
                          'expected_value':'BIGINT',  'convert_to_dialect':dialect.Mysql}], 
         
         dialect.Hive: [
                        {'input_value':'INT', 
                         'expected_value':'INT',  'convert_to_dialect':dialect.Mysql},
                        {'input_value':'INTEGER', 
                         'expected_value':'INT',  'convert_to_dialect':dialect.Mysql},
                        {'input_value':'VARCHAR', 
                         'expected_value':'VARCHAR',  'convert_to_dialect':dialect.Mysql},
                        {'input_value':'CHAR', 
                         'expected_value':'VARCHAR',  'convert_to_dialect':dialect.Mysql},
                        {'input_value':'STRING', 
                         'expected_value':'VARCHAR',  'convert_to_dialect':dialect.Mysql},
                        {'input_value':'INT', 
                         'expected_value':'int',  'convert_to_dialect':dialect.Mssql},
                        {'input_value':'INTEGER', 
                         'expected_value':'int',  'convert_to_dialect':dialect.Mssql},
                        {'input_value':'VARCHAR', 
                         'expected_value':'varchar',  'convert_to_dialect':dialect.Mssql},
                        {'input_value':'CHAR', 
                         'expected_value':'varchar',  'convert_to_dialect':dialect.Mssql},
                        {'input_value':'STRING', 
                         'expected_value':'varchar',  'convert_to_dialect':dialect.Mssql},
                        {'input_value':'DOUBLE', 
                         'expected_value':'float',  'convert_to_dialect':dialect.Mssql},
                        {'input_value':'DOUBLE PRECISION', 
                         'expected_value':'float',  'convert_to_dialect':dialect.Mssql}]}
        with self.assertRaises(exceptions.TYPE_NOT_DEFINED):
            sqlType.convert_type_string('foo', dialect.Mssql, dialect.Mysql)
        for key, values in conversions.items():
            for case in values:
                self.assertEqual(sqlType.convert_type_string(case['input_value'], key, case['convert_to_dialect']), case['expected_value'])


class TestSqlStringTypeMethods(unittest.TestCase):

    def test_type_specific_string_action(self):
        string = sqlType.STRING()
        self.assertIsNone(string.size)
        string.type_specific_string_action(dialect.Mssql)
        self.assertEqual(string.size, 'max')