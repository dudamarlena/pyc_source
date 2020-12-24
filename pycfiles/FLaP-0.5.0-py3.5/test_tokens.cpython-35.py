# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\latex\test_tokens.py
# Compiled at: 2016-10-19 08:12:51
# Size of source mod 2**32: 1712 bytes
from unittest import TestCase, main
from flap.latex.commons import Position
from flap.latex.tokens import *

class TokenTests(TestCase):

    def setUp(self):
        self._tokens = TokenFactory(SymbolTable.default())
        self._token = self._tokens.character(Position(1, 1), 'a')

    def test_equals_itself(self):
        self.assertEqual(self._token, self._token)

    def test_equals_a_similar_tokens(self):
        self.assertEqual(self._tokens.character(Position(1, 1), 'a'), self._token)

    def test_differs_from_a_different_character(self):
        self.assertNotEqual(self._tokens.character(Position(1, 1), 'b'), self._token)

    def test_differs_from_an_object_of_another_type(self):
        self.assertNotEquals('foo', self._token)

    def test_print_properly(self):
        self.assertEqual(Token.DISPLAY.format(text='a', category='character', location=Position(1, 1)), repr(self._token))


if __name__ == '__main__':
    main()