# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_trusted_keys.py
# Compiled at: 2019-11-22 14:51:16
"""
File: isc_trusted_keys.py

Clause: trusted-keys

Title: Statement for Trusted Keys

Description: Provides trusted-key-related grammar in
             PyParsing engine for ISC-configuration style
"""
from pyparsing import Word, alphanums, Group, Keyword, Literal, ZeroOrMore
from bind9_parser.isc_utils import semicolon, parse_me, lbrack, rbrack, number_type, squote, dquote, Combine, ungroup
from bind9_parser.isc_domain import rr_domain_name_or_wildcard_type
trusted_keyname_type = (rr_domain_name_or_wildcard_type | Literal('.'))('domain')
trusted_keyname_type.setName('<domain_name>')
trusted_keyname_dquoted = Combine(Literal('"').suppress() - trusted_keyname_type + Literal('"').suppress())
trusted_keyname_squoted = Combine(Literal("'").suppress() - trusted_keyname_type + Literal("'").suppress())
trusted_key_domain_name = Group(trusted_keyname_dquoted | trusted_keyname_squoted | trusted_keyname_type)
trusted_key_flags_type = number_type('flags')
trusted_key_flags_type.setName('<key-flags-id>')
trusted_key_protocol_type = number_type('protocol_id')
trusted_key_protocol_type.setName('<key-protocol-id>')
trusted_key_algorithm_name = Word(alphanums + '-')('algorithm')
trusted_key_algorithm_name.setName('<key-algorithm>')
trusted_key_algorithm_type = number_type('algorithm_id')
trusted_key_algorithm_type.setName('<key-algorithm-id>')
charset_key_secret_base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
charset_key_secret_base_squote_allowed = charset_key_secret_base + "'"
charset_key_secret_base_dquote_allowed = charset_key_secret_base + '"'
quoted_trusted_key_secret_type = Combine(squote + Word(charset_key_secret_base_dquote_allowed) + squote) | Combine(dquote + Word(charset_key_secret_base_squote_allowed) + dquote)
quoted_trusted_key_secret_type.setName('<quoted-key-secret>')
trusted_keys_statements_set = (Keyword('trusted-keys').suppress() + lbrack + Group(ungroup(trusted_key_domain_name)('domain') + trusted_key_flags_type - trusted_key_protocol_type - trusted_key_algorithm_type - quoted_trusted_key_secret_type + semicolon)('') + rbrack + semicolon)('trusted_keys')
trusted_keys_statements_series = ZeroOrMore(trusted_keys_statements_set)('trusted_keys')