# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_server.py
# Compiled at: 2019-11-22 14:51:11
"""
File: isc_server.py

Clause: server

Title: Statements Used Only By server Clause.

Description: Provides server-related grammar in PyParsing engine
             for ISC-configuration style
"""
from pyparsing import Group, Keyword, Word, nums, Optional, Literal, ZeroOrMore
from bind9_parser.isc_utils import isc_boolean, semicolon, number_type, key_id, byte_type
from bind9_parser.isc_inet import ip4_addr_or_wildcard, ip6_addr_or_wildcard, inet_ip_port_keyword_and_wildcard_element, inet_dscp_port_keyword_and_number_element
server_stmt_bogus = Keyword('bogus') - isc_boolean('bogus') + semicolon
server_stmt_edns = Keyword('edns') - isc_boolean('edns') + semicolon
server_stmt_edns_version = Keyword('edns-version') - byte_type('edns_version') + semicolon
server_stmt_keys = Keyword('keys') + key_id('keys') + semicolon
max_udp_size = number_type
server_stmt_max_udp_size = Keyword('max-udp-size') - max_udp_size('max_udp_size') + semicolon
server_stmt_notify_source = Keyword('notify-source') + Group(ip4_addr_or_wildcard('addr') + Optional(inet_ip_port_keyword_and_wildcard_element) + Optional(inet_dscp_port_keyword_and_number_element))('notify_source') + semicolon
server_stmt_notify_source_v6 = Keyword('notify-source-v6') + Group(ip6_addr_or_wildcard('addr') + Optional(inet_ip_port_keyword_and_wildcard_element) + Optional(inet_dscp_port_keyword_and_number_element))('notify_source_v6') + semicolon
server_stmt_padding = Keyword('padding') + number_type('padding') + semicolon
server_stmt_query_source = (Keyword('query-source') + Group(ip4_addr_or_wildcard('ip4_addr_w') - Optional(inet_ip_port_keyword_and_wildcard_element) - Optional(inet_dscp_port_keyword_and_number_element('dscp_port')) + semicolon | (Keyword('address').suppress() - ip4_addr_or_wildcard('ip4_addr_w') - Optional(inet_ip_port_keyword_and_wildcard_element) - Optional(inet_dscp_port_keyword_and_number_element('dscp_port')) + semicolon)(''))('query_source'))('')
server_stmt_query_source_v6 = (Keyword('query-source-v6') + Group(Keyword('address').suppress() - ip6_addr_or_wildcard('ip6_addr_w') - Optional(inet_ip_port_keyword_and_wildcard_element) - Optional(inet_dscp_port_keyword_and_number_element('dscp_port')) + semicolon | (ip6_addr_or_wildcard('ip6_addr_w') - Optional(inet_ip_port_keyword_and_wildcard_element) - Optional(inet_dscp_port_keyword_and_number_element('dscp_port')) + semicolon)(''))('query_source_v6'))('')
server_stmt_request_expire = Keyword('request-expire') - isc_boolean('request_expire') + semicolon
server_stmt_request_nsid = Keyword('request-nsid') + isc_boolean('request_nsid') + semicolon
server_stmt_send_cookie = Keyword('send-cookie') + isc_boolean('send_cookie') + semicolon
server_stmt_tcp_keepalive = Keyword('tcp-keepalive') + isc_boolean('tcp_keepalive') + semicolon
server_stmt_tcp_only = Keyword('tcp-only') + isc_boolean('tcp_only') + semicolon
server_stmt_transfer_source = (Keyword('transfer-source').suppress() - Group(ip4_addr_or_wildcard('ip4_addr_w') + Optional(inet_ip_port_keyword_and_wildcard_element) + Optional(inet_dscp_port_keyword_and_number_element))('transfer_source') + semicolon)('')
server_stmt_transfer_source_v6 = Keyword('transfer-source-v6').suppress() - Group(ip6_addr_or_wildcard('ip6_addr_w') + Optional(inet_ip_port_keyword_and_wildcard_element) + Optional(inet_dscp_port_keyword_and_number_element))('transfer_source_v6') + semicolon
server_stmt_transfers = Keyword('transfers') - number_type('transfers') + semicolon
server_statement_set = server_stmt_bogus ^ server_stmt_edns_version ^ server_stmt_edns ^ server_stmt_keys ^ server_stmt_max_udp_size ^ server_stmt_notify_source_v6 ^ server_stmt_notify_source ^ server_stmt_padding ^ server_stmt_query_source_v6 ^ server_stmt_query_source ^ server_stmt_request_expire ^ server_stmt_request_nsid ^ server_stmt_send_cookie ^ server_stmt_tcp_keepalive ^ server_stmt_tcp_only ^ server_stmt_transfer_source_v6 ^ server_stmt_transfer_source ^ server_stmt_transfers
server_statement_series = ZeroOrMore(server_statement_set)