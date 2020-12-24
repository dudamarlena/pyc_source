# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_viewzone.py
# Compiled at: 2019-11-22 14:51:38
"""
File: isc_viewzone.py

Clause: view, zone

Title: Statements Used Only By view And zone Clauses

Description: isc_viewzone contains all parse elements pertaining
             to both options and zone (but not view)
"""
from pyparsing import Group, CaselessKeyword, OneOrMore, Keyword
from bind9_parser.isc_utils import semicolon, database_name_type
from bind9_parser.isc_clause_dlz import dlz_name_type
viewzone_stmt_database = Keyword('database').suppress() - database_name_type('database') + semicolon
viewzone_stmt_dlz = CaselessKeyword('dlz').suppress() - dlz_name_type('dlz') + semicolon
viewzone_statements_set = viewzone_stmt_database | viewzone_stmt_dlz
viewzone_statements_series = OneOrMore(viewzone_statements_set)