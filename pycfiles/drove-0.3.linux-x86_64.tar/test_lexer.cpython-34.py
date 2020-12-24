# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/util/test_lexer.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1736 bytes
import unittest
from drove.util.lexer import Lexer

class ExampleItem(object):

    def __init__(self, arg):
        self.item = 'example'


class TestLexer(unittest.TestCase):

    def test_lexer(self):
        """Testing util.lexer.Lexer: basic behaviour"""
        x = Lexer()
        items = [i for i in x.parse('item1 arg1, item2 arg2.')]
        for item in items:
            if not item.__class__.__name__ == 'LexerItem':
                raise AssertionError

        assert [y.item for y in items] == ['arg1', 'arg2']

    def test_lexer_without_term(self):
        """Testing util.lexer.Lexer: without terminator"""
        x = Lexer()
        items = [i for i in x.parse('item1 arg1, item2 arg2')]
        for item in items:
            if not item.__class__.__name__ == 'LexerItem':
                raise AssertionError

        assert [y.item for y in items] == ['arg1', 'arg2']

    def test_lexer_add_parser(self):
        """Testing util.lexer.Lexer: addItemParser()"""
        x = Lexer()
        x.addItemParser('item1', ExampleItem)
        items = [i for i in x.parse('item1 arg1, item2 arg2')]
        assert [y.__class__.__name__ for y in items] == [
         'ExampleItem', 'LexerItem']
        assert [y.item for y in items] == ['example', 'arg2']

    def test_lexer_ignore_words(self):
        """Testing util.lexer.Lexer: addItemParser() with ignore_words"""
        x = Lexer()
        x.addItemParser('item1', ExampleItem, ignore_words=['ignore'])
        items = [i for i in x.parse('item1 ignore arg1.')]
        assert [y.__class__.__name__ for y in items] == ['ExampleItem']
        items = [i for i in x.parse('item1 arg1 ignore.')]
        assert [y.__class__.__name__ for y in items] == ['ExampleItem']