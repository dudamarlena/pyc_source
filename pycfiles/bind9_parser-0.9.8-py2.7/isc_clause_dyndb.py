# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_dyndb.py
# Compiled at: 2019-11-22 14:48:25
"""
File: isc_clause_dyndb.py

Clause: dyndb

Title: Clause statement for Dynamic Database

Description:
"""
import unittest
from pyparsing import Group, Keyword, Word, ZeroOrMore, OneOrMore
from bind9_parser.isc_utils import lbrack, rbrack, semicolon, isc_file_name, quoted_path_name, charset_filename_base
dyndb_custom_driver_configuration = (lbrack + Word(charset_filename_base + ' \t\r\n/;""\'')('driver_parameters') + rbrack)(None)
dyndb_database_name = isc_file_name('db_name')
dyndb_dynamic_module_name = quoted_path_name('module_filename')
clause_stmt_dyndb_standalone = (Keyword('dyndb').suppress() + Group(dyndb_database_name - dyndb_dynamic_module_name - dyndb_custom_driver_configuration) + semicolon)('dyndb')
clause_stmt_dyndb_series = OneOrMore(clause_stmt_dyndb_standalone)('dyndb')
if __name__ == '__main__':
    unittest.main()