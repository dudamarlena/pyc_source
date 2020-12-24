# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lexical/tests/sql_test.py
# Compiled at: 2017-09-29 11:43:39
import unittest, lexical, re
sql_tokens = [
 dict(type='T_SELECT', regex='^(SELECT)\\s', store=True, flags=re.I),
 dict(type='T_FROM', regex='^(FROM)\\s', store=True, flags=re.I),
 dict(type='T_WILDCARD', regex='^(\\*)\\s', store=True),
 dict(type='T_LABEL', regex='^([a-z]+)\\s', store=True),
 dict(type='T_ENDLINE', regex='^(\\n)', store=False),
 dict(type='T_WHITESPACE', regex='^([ \\t\\r])+', store=False)]

class SQLTest(unittest.TestCase):

    def test_select_all_fields_from_table(self):
        query = 'SELECT * FROM table'
        analysis = lexical.analyse(query, sql_tokens)
        tokens = list(analysis)
        self.assertEquals(4, len(tokens))
        self.assertEquals('T_SELECT', tokens[0]['type'])
        self.assertEquals('T_WILDCARD', tokens[1]['type'])
        self.assertEquals('T_FROM', tokens[2]['type'])
        self.assertEquals('T_LABEL', tokens[3]['type'])

    def test_select_all_fields_with_lower_case(self):
        query = 'select * from table'
        analysis = lexical.analyse(query, sql_tokens)
        tokens = list(analysis)
        self.assertEquals(4, len(tokens))
        self.assertEquals('T_SELECT', tokens[0]['type'])
        self.assertEquals('T_WILDCARD', tokens[1]['type'])
        self.assertEquals('T_FROM', tokens[2]['type'])
        self.assertEquals('T_LABEL', tokens[3]['type'])

    def test_select_all_fields_with_lower_case(self):
        query = 'selectfrom'
        analysis = lexical.analyse(query, sql_tokens)
        tokens = list(analysis)
        self.assertEquals('T_LABEL', tokens[0]['type'])