# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_optzone.py
# Compiled at: 2019-11-22 14:51:01
"""
File: isc_optzone.py

Clause: options, zone

Title: Statements Used Only By options And zone Clauses.

Description: isc_optzone contains all parse elements pertaining
             to both options and zone (but not view)
"""
from pyparsing import Group, Keyword, OneOrMore
from bind9_parser.isc_utils import isc_boolean, semicolon, parse_me
optzone_stmt_notify_to_soa = Keyword('notify-to-soa') - isc_boolean('notify_to_soa') + semicolon
optzone_statements_set = optzone_stmt_notify_to_soa
optzone_statements_series = OneOrMore(optzone_statements_set)