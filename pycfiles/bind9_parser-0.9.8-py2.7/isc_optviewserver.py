# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_optviewserver.py
# Compiled at: 2019-11-22 14:50:43
"""
File: isc_optviewserver.py

Clause: options

Title: Statements Used Only By options, view, And server Clauses.

Description: Provides 'options' and 'server'-related grammar in
             PyParsing engine for ISC-configuration style
"""
from pyparsing import ZeroOrMore, Keyword, Literal
from bind9_parser.isc_utils import semicolon, isc_boolean, number_type
optviewserver_stmt_edns_udp_size = Keyword('edns-udp-size') - number_type('edns_udp_size') + semicolon
optviewserver_stmt_provide_ixfr = Keyword('provide-ixfr') - isc_boolean('provide_ixfr') + semicolon
optviewserver_stmt_request_ixfr = Keyword('request-ixfr') + isc_boolean('request_ixfr') + semicolon
optviewserver_stmt_transfer_format = Keyword('transfer-format') + (Literal('one-answer') | Literal('many-answers'))('transfer_format') + semicolon
optviewserver_statements_set = optviewserver_stmt_provide_ixfr | optviewserver_stmt_request_ixfr | optviewserver_stmt_transfer_format | optviewserver_stmt_edns_udp_size
optviewserver_statements_series = ZeroOrMore(optviewserver_statements_set)