# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_optviewzoneserver.py
# Compiled at: 2019-11-22 14:50:55
"""
File: isc_optviewzoneserver.py

Clause: options, view, zone, server

Title:  Statements Used Only By options, view, zone, And server Clauses

Description: Provides statement support for ones found in all
             four clauses: options, view, zone, server
             PyParsing engine for ISC-configuration style
"""
from pyparsing import Group, Keyword, OneOrMore, ZeroOrMore, Optional, ungroup
from bind9_parser.isc_utils import semicolon, lbrack, rbrack, parse_me
from bind9_parser.isc_clause_key import key_id
from bind9_parser.isc_inet import ip46_addr, inet_ip_port_keyword_and_number_element, inet_dscp_port_keyword_and_number_element
from bind9_parser.isc_clause_masters import master_id
optviewzoneserver_stmt_also_notify_element_set = (ip46_addr('addr') | master_id('addr')) + Optional(inet_ip_port_keyword_and_number_element) - Optional(inet_dscp_port_keyword_and_number_element) + Optional(Keyword('key') + key_id) + semicolon
optviewzoneserver_also_notify_element_series = OneOrMore(Group(optviewzoneserver_stmt_also_notify_element_set))
optviewzoneserver_stmt_also_notify = (Keyword('also-notify').suppress() - Optional(inet_ip_port_keyword_and_number_element) - Optional(inet_dscp_port_keyword_and_number_element) + lbrack - optviewzoneserver_also_notify_element_series + rbrack + semicolon)('also_notify')
optviewzoneserver_statements_set = optviewzoneserver_stmt_also_notify
optviewzoneserver_statements_series = OneOrMore(optviewzoneserver_statements_set)