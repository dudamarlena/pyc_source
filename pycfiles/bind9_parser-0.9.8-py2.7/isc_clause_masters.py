# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_masters.py
# Compiled at: 2019-11-22 14:48:43
"""
File: isc_clause_masters.py

Clause: masters

Title: Clause Statement for Master Servers

Description: Provides master-related grammar in PyParsing engine
             for ISC-configuration style
"""
from pyparsing import OneOrMore, Group, Keyword, Optional, Word, srange, Combine, ZeroOrMore, ungroup
from bind9_parser.isc_utils import lbrack, rbrack, semicolon, dquote, squote, key_id_keyword_and_name_pair
from bind9_parser.isc_inet import ip4_addr, ip6_addr, ip46_addr, inet_ip_port_keyword_and_number_element, inet_dscp_port_keyword_and_number_element
from bind9_parser.isc_rr import rr_domain_name_or_root
charset_master_name = srange('[A-Za-z0-9]') + '_-.'
master_name_type = Word(charset_master_name)('master_name_type')
master_name_type.setName('<master_name>')
master_name_type_squotable = Word(charset_master_name + '"')
master_name_type_dquotable = Word(charset_master_name + "'")
master_name_type_with_squote = Combine(dquote - master_name_type_dquotable + dquote)
master_name_type_with_dquote = Combine(squote - master_name_type_squotable + squote)
master_id = (master_name_type_squotable | master_name_type_dquotable | master_name_type)('master_id')
masters_element_list = ip4_addr('addr') + Optional(inet_ip_port_keyword_and_number_element) + Optional(key_id_keyword_and_name_pair) + semicolon | ip6_addr('addr') + Optional(inet_ip_port_keyword_and_number_element) + Optional(key_id_keyword_and_name_pair) + semicolon | master_id('addr') + Optional(key_id_keyword_and_name_pair) + semicolon | master_id('addr') + semicolon
masters_element_series = OneOrMore(Group(masters_element_list))('master_list')
clause_stmt_masters_standalone = (Keyword('masters').suppress() - Group(master_id('master_id') - Optional(inet_ip_port_keyword_and_number_element) - Optional(inet_dscp_port_keyword_and_number_element) - Group(lbrack + masters_element_series('') + rbrack)('master_list')) + semicolon)('masters')
clause_stmt_masters_series = OneOrMore(clause_stmt_masters_standalone)('masters')
clause_stmt_masters_series.setName('masters <name> key <key_id>')