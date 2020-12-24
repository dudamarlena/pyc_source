# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_trusted_keys.py
# Compiled at: 2019-11-22 14:49:40
"""
File: isc_clause_trusted_keys.py

Clause: trusted-keys

Title: Clause Statement for Trusted Keys

Description: Provides trusted-key-related grammar in
             PyParsing engine for ISC-configuration style
"""
from pyparsing import Word, alphanums, Group, Keyword, Literal, ZeroOrMore
from bind9_parser.isc_utils import semicolon, parse_me, lbrack, rbrack, number_type, squote, dquote, Combine
from bind9_parser.isc_domain import rr_domain_name_or_wildcard_type
from bind9_parser.isc_trusted_keys import trusted_keys_statements_set, trusted_keys_statements_series
clause_stmt_trusted_keys_standalone = trusted_keys_statements_set('trusted_keys')
clause_stmt_trusted_keys_series = ZeroOrMore(clause_stmt_trusted_keys_standalone)('trusted_keys')