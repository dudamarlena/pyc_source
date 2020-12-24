# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_aml.py
# Compiled at: 2019-11-22 14:47:48
"""
File: isc_aml.py

Clause: controls, options, view, zone

Element: aml

Title: AML For controls, options, view, And zone Clauses

Description: Provides Address Match List (AML)-related grammar in
             PyParsing engine for ISC-configuration style
"""
from pyparsing import ZeroOrMore, Forward, Group, CaselessLiteral
from bind9_parser.isc_utils import semicolon, lbrack, rbrack, exclamation, acl_name
from bind9_parser.isc_inet import ip4_addr, ip6_addr, ip4s_prefix
literal_localhost = CaselessLiteral('localhost')('').setName('"localhost"')
literal_any = CaselessLiteral('any')('')
literal_any.setName('"any"')
literal_none = CaselessLiteral('none')('')
literal_none.setName('"none"')
literal_localnets = CaselessLiteral('localnets')('')
literal_localnets.setName('"localnets"')
aml_choices_key_id = CaselessLiteral('key').suppress() + acl_name('')
aml_choices_key_id.setName('"key" <key_id>')
aml_choices_acl_name = acl_name('')
aml_choices = aml_choices_key_id('key_id') | ip4s_prefix('addr') | ip4_addr('addr') | ip6_addr('addr') | literal_any('addr') | literal_none('addr') | literal_localhost('addr') | literal_localnets('addr') | aml_choices_acl_name('acl_name')
aml_nesting = Forward()
aml_nesting << (lbrack + ZeroOrMore(Group(exclamation('not') + aml_nesting | exclamation('not') + aml_choices + semicolon | aml_nesting | aml_choices + semicolon))(None)('aml') + rbrack + semicolon)(None)