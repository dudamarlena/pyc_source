# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\latex\test_lexer.py
# Compiled at: 2016-12-16 08:57:15
# Size of source mod 2**32: 5765 bytes
from unittest import TestCase, main
from flap.latex.commons import Position, Source
from flap.latex.symbols import SymbolTable
from flap.latex.tokens import TokenFactory
from flap.latex.lexer import Lexer

class LexerTests(TestCase):

    def setUp(self):
        self._symbols = SymbolTable.default()
        self._tokens = TokenFactory(self._symbols)
        self._text = None

    def _on_take(self, character):
        if character in self._symbols.NEW_LINE:
            self._position = self._position.new_line
        else:
            self._position = self._position.new_character

    def test_recognises_a_single_character(self):
        self._text = 'b'
        self._verify_tokens(self._tokens.character(Position(1, 1), 'b'))

    def test_recognises_a_word(self):
        self._text = 'hello'
        self._verify_tokens(self._tokens.character(Position(1, 1), 'h'), self._tokens.character(Position(1, 2), 'e'), self._tokens.character(Position(1, 3), 'l'), self._tokens.character(Position(1, 4), 'l'), self._tokens.character(Position(1, 5), 'o'))

    def test_recognises_a_single_command(self):
        self._text = '\\myMacro'
        self._verify_tokens(self._tokens.command(Position(1, 1), '\\myMacro'))

    def test_recognises_a_single_special_character_command(self):
        self._text = '\\%'
        self._verify_tokens(self._tokens.command(Position(1, 1), '\\%'))

    def test_recognises_sequences_of_single_character_command(self):
        self._text = '\\%\\$\\\\'
        self._verify_tokens(self._tokens.command(Position(1, 1), '\\%'), self._tokens.command(Position(1, 3), '\\$'), self._tokens.command(Position(1, 5), '\\\\'))

    def test_recognises_two_commands(self):
        self._text = '\\def\\foo'
        self._verify_tokens(self._tokens.command(Position(1, 1), '\\def'), self._tokens.command(Position(1, 5), '\\foo'))

    def test_recognises_two_commands_separated_by_white_spaces(self):
        self._text = '\\def  \t  \\foo'
        self._verify_tokens(self._tokens.command(Position(1, 1), '\\def'), self._tokens.white_space(Position(1, 5), '  \t  '), self._tokens.command(Position(1, 14), '\\foo'))

    def test_recognises_a_comment(self):
        self._text = '%This is a comment\n\\def\\foo'
        self._verify_tokens(self._tokens.comment(Position(1, 1), '%This is a comment'), self._tokens.new_line(Position(1, 1)), self._tokens.command(Position(2, 1), '\\def'), self._tokens.command(Position(2, 5), '\\foo'))

    def test_recognises_an_opening_group(self):
        self._text = '{'
        self._verify_tokens(self._tokens.begin_group(Position(1, 1)))

    def test_recognises_an_ending_group(self):
        self._text = '}'
        self._verify_tokens(self._tokens.end_group(Position(1, 1)))

    def test_recognises_an_parameter(self):
        self._text = '\\def#1'
        self._verify_tokens(self._tokens.command(Position(1, 1), '\\def'), self._tokens.parameter(Position(1, 5), '#1'))

    def test_recognises_a_complete_macro_definition(self):
        self._text = '\\def\\point#1#2{(#2,#1)}'
        self._verify_tokens(self._tokens.command(Position(1, 1), '\\def'), self._tokens.command(Position(1, 5), '\\point'), self._tokens.parameter(Position(1, 11), '#1'), self._tokens.parameter(Position(1, 13), '#2'), self._tokens.begin_group(Position(1, 15), '{'), self._tokens.others(Position(1, 16), '('), self._tokens.parameter(Position(1, 17), '#2'), self._tokens.others(Position(1, 19), ','), self._tokens.parameter(Position(1, 20), '#1'), self._tokens.others(Position(1, 22), ')'), self._tokens.end_group(Position(1, 23), '}'))

    def test_recognises_math_mode(self):
        self._text = '$'
        self._verify_tokens(self._tokens.math(Position(1, 1)))

    def test_recognises_superscript(self):
        self._text = '^'
        self._verify_tokens(self._tokens.superscript(Position(1, 1)))

    def test_recognises_subscript(self):
        self._text = '_'
        self._verify_tokens(self._tokens.subscript(Position(1, 1)))

    def test_recognises_non_breaking_space(self):
        self._text = '~'
        self._verify_tokens(self._tokens.non_breaking_space(Position(1, 1)))

    def _verify_tokens(self, *expected_tokens):
        self.assertListEqual(list(expected_tokens), list(Lexer(self._symbols, Source(self._text))))


if __name__ == '__main__':
    main()