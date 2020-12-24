# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_key.py
# Compiled at: 2019-11-22 14:48:29
"""
File: isc_clause_key.py

Clause: keys

Title: Clause statement for key

Description: Provides key-related grammar in PyParsing engine
             for ISC-configuration style
"""
from pyparsing import Word, alphanums, Group, Keyword, ZeroOrMore
from bind9_parser.isc_utils import semicolon, lbrack, rbrack, key_id, key_secret
key_algorithm_name = Word(alphanums + '-')('algorithm')
key_algorithm_name.setName('<key-algorithm>')
key_algorithm_element = Keyword('algorithm').suppress() - key_algorithm_name('algorithm') + semicolon
key_algorithm_element.setName('algorithm <key-algorithm>;')
key_secret_element = Keyword('secret').suppress() - key_secret('secret') + semicolon
key_secret_element.setName('secret <key_secret>;')
clause_stmt_key_standalone = (Keyword('key').suppress() - Group(key_id('key_id') + lbrack - key_algorithm_element - key_secret_element + rbrack) + semicolon)('key')
clause_stmt_key_series = ZeroOrMore(clause_stmt_key_standalone)('key')
clause_stmt_key_series.setName('key <key-name> { algorithm <string>; secret <key-secret>; };')