# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flap\latex\symbols.py
# Compiled at: 2016-12-19 08:02:24
# Size of source mod 2**32: 3297 bytes
from enum import Enum, unique

@unique
class Symbol(Enum):
    CHARACTER = 0
    BEGIN_GROUP = 1
    COMMENT = 2
    CONTROL = 3
    END_GROUP = 4
    END_OF_TEXT = 5
    MATH = 6
    NEW_LINE = 7
    NON_BREAKING_SPACE = 8
    OTHERS = 9
    PARAMETER = 10
    SUBSCRIPT = 11
    SUPERSCRIPT = 12
    WHITE_SPACES = 13


class SymbolTable:
    __doc__ = '\n    Characters recognised by (La)TeX, augmented with some relevant for parsing such new lines.\n    '

    @staticmethod
    def character_range(start, end):
        return [chr(code) for code in range(ord(start), ord(end) + 1)]

    @staticmethod
    def default():
        return SymbolTable({Symbol.BEGIN_GROUP: ['{'], 
         Symbol.CHARACTER: SymbolTable.character_range('a', 'z') + SymbolTable.character_range('A', 'Z'), 
         Symbol.COMMENT: ['%'], 
         Symbol.CONTROL: ['\\'], 
         Symbol.END_GROUP: ['}'], 
         Symbol.MATH: ['$'], 
         Symbol.NEW_LINE: ['\n'], 
         Symbol.NON_BREAKING_SPACE: ['~'], 
         Symbol.PARAMETER: ['#'], 
         Symbol.SUBSCRIPT: ['_'], 
         Symbol.SUPERSCRIPT: ['^'], 
         Symbol.WHITE_SPACES: [' ', '\t']})

    def __init__(self, symbols):
        self._symbols = symbols

    def __getitem__(self, key):
        assert key in list(Symbol), 'Symbol table only maps symbol categories to symbol lists'
        return self._symbols[key]

    def __setitem__(self, key, value):
        assert key in list(Symbol), 'Symbol table only maps symbol categories to symbol lists'
        self._symbols[key] = value

    def match(self, character, category):
        return character in self._symbols[category]

    def category_of(self, character):
        for category, markers in self._symbols.items():
            if character in markers:
                return category

        return Symbol.OTHERS

    @property
    def end_of_text(self):
        return self.get(Symbol.END_OF_TEXT)

    def get(self, category):
        return self._symbols[category][0]

    def __getattr__(self, item):
        """
        Expose the entries of the internal _tokens dictionary as attributes.

        With this, we access the list of character defined for one category
        >>> table = SymbolTable.default()
        >>> table.CHARACTER

        instead of:
        >>> table[Symbol.CHARACTER]
        """
        if item in [each.name for each in list(Symbol)]:
            return self._symbols[Symbol[item]]
        return self.__getattribute__(item)