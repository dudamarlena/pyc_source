# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause.py
# Compiled at: 2019-11-23 15:57:43
"""
File: isc_clause.py

Clause: top-level

Title: Clause Statement for all clauses

Description: Provides ALL clauses at the top-level of ISC
             configuration file (isc_clause_*.py)
"""
from pyparsing import ZeroOrMore, OneOrMore, Group, ungroup
from bind9_parser.isc_clause_acl import clause_stmt_acl_standalone
from bind9_parser.isc_clause_controls import clause_stmt_control_standalone
from bind9_parser.isc_clause_dlz import clause_stmt_dlz_standalone
from bind9_parser.isc_clause_dyndb import clause_stmt_dyndb_standalone
from bind9_parser.isc_clause_key import clause_stmt_key_standalone
from bind9_parser.isc_clause_logging import clause_stmt_logging_standalone
from bind9_parser.isc_clause_managed_keys import clause_stmt_managed_keys_standalone
from bind9_parser.isc_clause_masters import clause_stmt_masters_standalone
from bind9_parser.isc_clause_options import clause_stmt_options
from bind9_parser.isc_clause_server import clause_stmt_server_standalone
from bind9_parser.isc_clause_trusted_keys import clause_stmt_trusted_keys_standalone
from bind9_parser.isc_clause_view import clause_stmt_view_standalone
from bind9_parser.isc_clause_zone import clause_stmt_zone_standalone, clause_stmt_zone_series
optional_clause_stmt_set = clause_stmt_acl_standalone | clause_stmt_control_standalone | clause_stmt_dlz_standalone | clause_stmt_dyndb_standalone | clause_stmt_key_standalone | clause_stmt_logging_standalone | clause_stmt_managed_keys_standalone | clause_stmt_masters_standalone | clause_stmt_server_standalone | clause_stmt_trusted_keys_standalone | clause_stmt_view_standalone | clause_stmt_zone_standalone('zones25')
optional_clause_stmt_series = OneOrMore(optional_clause_stmt_set)
mandatory_clause_stmt_set = clause_stmt_options
clause_statements = ZeroOrMore(optional_clause_stmt_set | mandatory_clause_stmt_set)