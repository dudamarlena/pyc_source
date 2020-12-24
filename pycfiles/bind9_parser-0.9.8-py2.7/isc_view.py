# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_view.py
# Compiled at: 2019-11-22 14:51:32
"""
File: isc_view.py

Clause: view

Title: Statements Used Only By view Clause.

Description: Provides View-related grammar in PyParsing engine
             for ISC-configuration style.

             Covers the statements that are only found in View
             clause (and no other clauses).

             Does not test for view_name (that is in
             isc_util.py/test_util.py) nor test for
             clause_stmt_view_standalone (that is in clause_view.py/test_clause_view.py)
"""
from pyparsing import Group, Keyword, ZeroOrMore
from bind9_parser.isc_utils import semicolon, isc_boolean
from bind9_parser.isc_aml import aml_nesting
from bind9_parser.isc_trusted_keys import trusted_keys_statements_set
view_stmt_match_clients = (Keyword('match-clients').suppress() - Group(aml_nesting(''))('match_clients'))('')
view_stmt_match_destinations = (Keyword('match-destinations').suppress() - Group(aml_nesting(''))('match_destinations'))('')
view_stmt_match_recursive_only = (Keyword('match-recursive-only').suppress() - isc_boolean('match_recursive_only') + semicolon)('')
view_statements_set = view_stmt_match_recursive_only | view_stmt_match_destinations | view_stmt_match_clients
view_statements_series = ZeroOrMore(view_statements_set)