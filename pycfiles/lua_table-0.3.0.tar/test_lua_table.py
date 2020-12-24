# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/archiv/2015/projekty/lua_table/test/test_lua_table.py
# Compiled at: 2015-01-26 05:18:24
from __future__ import print_function, unicode_literals
import logging, pickle, unittest
from collections import OrderedDict
from rply import Token
from lua_table import lexer, parser, parse
INSTR = b'\nreturn {\n\t["password"] = "secret";\n}\n'

class TestLuaTebleLexer(unittest.TestCase):

    def test_lex_simple(self):
        tokens = list(lexer.lex(INSTR))
        self.assertEqual(tokens, [Token(b'RETURN', b'return'),
         Token(b'OPBRACE', b'{'),
         Token(b'OPBRAK', b'['),
         Token(b'STRING', b'"password"'),
         Token(b'CLBRAK', b']'),
         Token(b'STRING', b'"secret"'),
         Token(b'RECSEP', b';'),
         Token(b'CLBRACE', b'}')])

    def test_lex_roster(self):
        with open(b'test/data/roster.dat') as (inf):
            with open(b'test/data/roster-lex.pkl', b'rb') as (expf):
                tokens = list(lexer.lex(inf.read()))
                expected = pickle.load(expf)
        self.assertEqual(tokens, expected)


class TestLuaTebleParser(unittest.TestCase):

    def test_parse_account(self):
        logging.debug(b'\n%s', b'=' * 60)
        with open(b'test/data/account.dat') as (inf):
            instr = inf.read()
            pars = parser.parse(lexer.lex(instr))
            self.assertEqual(pars, OrderedDict([('password', 'secret')]))

    def test_parse_bigger_record(self):
        logging.debug(b'\n%s', b'=' * 60)
        with open(b'test/data/multi-value.dat') as (inf):
            pars = parser.parse(lexer.lex(inf.read()))
            expected = OrderedDict([
             (
              b'lady01@bastards.com',
              OrderedDict([('subscription', 'both'),
               (
                b'groups', OrderedDict([(b'Church', True)])),
               ('name', "Joan d'Arc")]))])
            logging.debug(b'pars = %s', pars)
            self.assertEqual(pars, expected)

    def test_parse_roster(self):
        logging.debug(b'\n%s', b'=' * 60)
        with open(b'test/data/roster.dat') as (inf):
            with open(b'test/data/roster-parse.pkl', b'rb') as (expf):
                expected = pickle.load(expf)
                tokens = lexer.lex(inf.read())
                pars = parser.parse(tokens)
                self.assertEqual(pars, expected)

    def test_parse_method(self):
        logging.debug(b'\n%s', b'=' * 60)
        with open(b'test/data/roster-parse.pkl', b'rb') as (expf):
            expected = pickle.load(expf)
            observed = parse(b'test/data/roster.dat')
            self.assertEqual(observed, expected)


if __name__ == b'__main__':
    unittest.main()