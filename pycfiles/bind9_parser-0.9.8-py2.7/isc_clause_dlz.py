# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_dlz.py
# Compiled at: 2019-11-22 14:48:16
"""
File: isc_dlz

Clause: dlz

Title: Clause statement for the DLZ

Description:
"""
from pyparsing import Group, CaselessKeyword, alphanums, Word, ZeroOrMore, OneOrMore
from bind9_parser.isc_utils import semicolon, name_type, isc_boolean, lbrack, rbrack, dlz_name_type, path_name
dlz_database_element = CaselessKeyword('database').suppress() - path_name('db_args') + semicolon
dlz_search_element = CaselessKeyword('search').suppress() - isc_boolean('search') + semicolon
dlz_element_group = dlz_search_element + dlz_database_element | dlz_database_element + dlz_search_element
clause_stmt_dlz_standalone = (CaselessKeyword('dlz').suppress() - Group(dlz_name_type('dlz_name') - lbrack - OneOrMore(dlz_element_group('')) + rbrack) + semicolon)('dlz')
clause_stmt_dlz_series = ZeroOrMore(clause_stmt_dlz_standalone)('dlz')