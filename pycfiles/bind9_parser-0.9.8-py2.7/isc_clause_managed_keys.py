# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_managed_keys.py
# Compiled at: 2019-11-22 14:48:36
"""
File: isc_clause_managed_keys.py

Clause: managed-keys

Title: Clause statement for managed keys

Description: Provides managed-key-related grammar in
             PyParsing engine for ISC-configuration style
"""
from pyparsing import Optional, OneOrMore, ZeroOrMore
from bind9_parser.isc_managed_keys import managed_keys_statement_standalone
clause_stmt_managed_keys_standalone = managed_keys_statement_standalone
clause_stmt_managed_keys_series = ZeroOrMore(managed_keys_statement_standalone)('managed_keys')