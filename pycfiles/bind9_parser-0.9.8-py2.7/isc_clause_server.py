# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_server.py
# Compiled at: 2019-11-22 14:49:17
"""
File: isc_clause_server.py

Clause: server

Title: Clause Statement for Server Definitions

Description:
"""
from pyparsing import OneOrMore, Keyword, ZeroOrMore, Group
from bind9_parser.isc_utils import lbrack, rbrack, semicolon, parse_me
from bind9_parser.isc_inet import ip46_addr_or_prefix
from bind9_parser.isc_server import server_statement_set
from bind9_parser.isc_optviewserver import optviewserver_statements_set
from bind9_parser.isc_optviewzoneserver import optviewzoneserver_statements_set
server_all_statements_set = optviewserver_statements_set | optviewzoneserver_statements_set | server_statement_set
server_all_statements_series = ZeroOrMore(server_all_statements_set)
clause_stmt_server_standalone = (Keyword('server').suppress() - Group(ip46_addr_or_prefix('addr') + lbrack + Group(server_all_statements_series)('configs') + rbrack)('') + semicolon)('server')
clause_stmt_server_standalone.setName('server { ... };')
clause_stmt_server_series = ZeroOrMore(clause_stmt_server_standalone)('server')
clause_stmt_server_series.setName('server { ... }; ...;')