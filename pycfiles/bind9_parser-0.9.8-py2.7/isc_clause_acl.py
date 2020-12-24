# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_clause_acl.py
# Compiled at: 2019-11-22 14:47:57
"""
File: isc_clause_acl.py

Clause: acl

Title: Clause statement for the Access Control List

Description: Provides clause-specific aspect of ACL-related grammar
             in PyParsing engine for ISC-configuration style.

             Reason for separate file from isc_acl is to avoid the Python
             'import' circular dependency of 'isc_aml'.
"""
from pyparsing import Group, ZeroOrMore, Literal, Word, alphanums, Keyword
from bind9_parser.isc_utils import acl_name
from bind9_parser.isc_aml import aml_nesting
clause_stmt_acl_standalone = (Keyword('acl').suppress() - Group(acl_name - ZeroOrMore(Group(aml_nesting(''))(''))('')('aml_series'))(''))('acl')
clause_stmt_acl_series = ZeroOrMore(clause_stmt_acl_standalone)('acl')