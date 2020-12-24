# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_controls.py
# Compiled at: 2019-11-22 14:48:06
"""
File: isc_clause_controls.py

Clause: controls

Title: Clause statement for the 'controls' connections.

Description
"""
from pyparsing import Keyword, Group, Optional, Literal, OneOrMore, ZeroOrMore
from bind9_parser.isc_utils import semicolon, lbrack, rbrack, isc_boolean, quoted_path_name, number_type, exclamation, key_id
from bind9_parser.isc_aml import aml_nesting, aml_choices
from bind9_parser.isc_inet import ip46_addr_or_wildcard, inet_ip_port_keyword_and_wildcard_element
controls_inet_addr_and_port = ip46_addr_or_wildcard('control_server_addr') + Optional(inet_ip_port_keyword_and_wildcard_element)
controls_inet_allow_element = Group(Keyword('allow').suppress() + lbrack + ZeroOrMore(Group(exclamation('not') + aml_nesting | exclamation('not') + aml_choices + semicolon | aml_nesting | aml_choices + semicolon))(None)('aml') + rbrack)('allow')
controls_keys_element = (Keyword('keys').suppress() + lbrack + ZeroOrMore(Group(key_id(None) + semicolon)) + rbrack)('keys')
controls_inet_read_only_element = Keyword('read-only').suppress() - isc_boolean('read-only')
controls_inet_set = Group(Keyword('inet').suppress() + controls_inet_addr_and_port(None) - controls_inet_allow_element(None) + Optional(controls_keys_element) + Optional(controls_inet_read_only_element) + semicolon)('inet')
controls_unix_set = Group(Keyword('unix').suppress() + (quoted_path_name('path_name') + Literal('perm').suppress() + number_type('perm') + Literal('owner').suppress() + number_type('uid') + Literal('group').suppress() + number_type('gid') - Optional(controls_keys_element) - Optional(controls_inet_read_only_element) + semicolon))('unix')
clause_stmt_control_standalone = Keyword('controls').suppress() + lbrack + Group(OneOrMore(Group(controls_inet_set('inet')) | Group(controls_unix_set('unix'))))('controls') + rbrack + semicolon
clause_stmt_control_series = ZeroOrMore(clause_stmt_control_standalone)