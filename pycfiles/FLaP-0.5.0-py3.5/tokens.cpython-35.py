# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\latex\tokens.py
# Compiled at: 2016-12-16 08:56:50
# Size of source mod 2**32: 4925 bytes
from flap.latex.symbols import Symbol, SymbolTable

class Token:
    __doc__ = 'All the possible tokens recognised by a TeX engine'
    DISPLAY = '{category}({text}){location}'

    def __init__(self, text, category, location):
        self._text = text
        self._category = category
        self._location = location

    @property
    def location(self):
        return self._location

    def satisfies(self, predicate):
        return predicate.evaluate_on(self._text, self._category, self._location)

    def is_a(self, category):
        return self._category == category

    @property
    def is_ignored(self):
        return self.is_a_whitespace or self.is_a_comment or self.is_a_new_line

    @property
    def is_a_comment(self):
        return self._category == Symbol.COMMENT

    @property
    def is_a_new_line(self):
        return self._category == Symbol.NEW_LINE

    @property
    def is_a_command(self):
        return self._category == Symbol.CONTROL

    def has_text(self, text):
        return self._text == text

    @property
    def ends_the_text(self):
        return self._category == Symbol.END_OF_TEXT

    @property
    def is_a_character(self):
        return self._category == Symbol.CHARACTER

    @property
    def is_a_parameter(self):
        return self._category == Symbol.PARAMETER

    @property
    def begins_a_group(self):
        return self._category == Symbol.BEGIN_GROUP

    @property
    def ends_a_group(self):
        return self._category == Symbol.END_GROUP

    @property
    def is_a_whitespace(self):
        return self._category == Symbol.WHITE_SPACES

    def __eq__(self, other_token):
        if not isinstance(other_token, Token):
            return False
        return self._text == other_token._text and self._category == other_token._category

    def __repr__(self):
        return self.DISPLAY.format(location=self._location, text=self._text, category=self._category.name.lower())

    def __str__(self):
        return self._text


class TokenFactory:

    def __init__(self, symbol_table):
        assert isinstance(symbol_table, SymbolTable)
        self._symbols = symbol_table

    @staticmethod
    def character(location, text):
        return Token(text, Symbol.CHARACTER, location)

    @staticmethod
    def command(location, text):
        return Token(text, Symbol.CONTROL, location)

    @staticmethod
    def white_space(location, text):
        return Token(text, Symbol.WHITE_SPACES, location)

    @staticmethod
    def comment(location, text):
        return Token(text, Symbol.COMMENT, location)

    def new_line(self, location, text=None):
        text = text if text else self._symbols.get(Symbol.NEW_LINE)
        return Token(text, Symbol.NEW_LINE, location)

    def begin_group(self, location, text=None):
        text = text if text else self._symbols.get(Symbol.BEGIN_GROUP)
        return Token(text, Symbol.BEGIN_GROUP, location)

    def end_group(self, location, text=None):
        text = text if text else self._symbols.get(Symbol.END_GROUP)
        return Token(text, Symbol.END_GROUP, location)

    @staticmethod
    def parameter(location, key):
        return Token(key, Symbol.PARAMETER, location)

    def math(self, location):
        text = self._symbols.get(Symbol.MATH)
        return Token(text, Symbol.MATH, location)

    def superscript(self, location, text=None):
        text = text if text else self._symbols.get(Symbol.SUPERSCRIPT)
        return Token(text, Symbol.SUPERSCRIPT, location)

    def subscript(self, location, text=None):
        text = text if text else self._symbols.get(Symbol.SUBSCRIPT)
        return Token(text, Symbol.SUBSCRIPT, location)

    def non_breaking_space(self, location, text=None):
        text = text if text else self._symbols.get(Symbol.NON_BREAKING_SPACE)
        return Token(text, Symbol.NON_BREAKING_SPACE, location)

    def others(self, location, text=None):
        text = text if text else self._symbols.get(Symbol.OTHERS)
        return Token(text, Symbol.OTHERS, location)