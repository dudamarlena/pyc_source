# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/parse/token.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1824 bytes
import enum
from exactly_lib.util.name import name_with_plural_s

class TokenType(enum.Enum):
    PLAIN = 0
    QUOTED = 1


class QuoteType(enum.Enum):
    SOFT = 1
    HARD = 2


SOFT_QUOTE_CHAR = '"'
HARD_QUOTE_CHAR = "'"
SOFT_QUOTE_NAME = name_with_plural_s('soft quote')
HARD_QUOTE_NAME = name_with_plural_s('hard quote')
QUOTE_CHARS = frozenset([SOFT_QUOTE_CHAR,
 HARD_QUOTE_CHAR])
QUOTE_CHAR_FOR_TYPE = {QuoteType.SOFT: SOFT_QUOTE_CHAR, 
 QuoteType.HARD: HARD_QUOTE_CHAR}
QUOTE_NAME_FOR_TYPE = {QuoteType.SOFT: SOFT_QUOTE_NAME, 
 QuoteType.HARD: HARD_QUOTE_NAME}

class Token(tuple):

    def __new__(cls, token_type: TokenType, string: str, source_string: str=None):
        return tuple.__new__(cls, (token_type,
         string,
         source_string if source_string is not None else string))

    @property
    def type(self) -> TokenType:
        return self[0]

    @property
    def is_plain(self) -> bool:
        return self.type is TokenType.PLAIN

    @property
    def is_quoted(self) -> bool:
        return self.type is TokenType.QUOTED

    @property
    def quote_type(self) -> QuoteType:
        """
        Precontition: is_quoted
        """
        if self[2][0] == SOFT_QUOTE_CHAR:
            return QuoteType.SOFT
        return QuoteType.HARD

    @property
    def is_hard_quote_type(self) -> bool:
        """
        Precontition: is_quoted
        """
        return self[2][0] == HARD_QUOTE_CHAR

    @property
    def string(self) -> str:
        return self[1]

    @property
    def source_string(self) -> str:
        return self[2]


class TokenMatcher:

    def matches(self, token: Token) -> bool:
        raise NotImplementedError('abstract method')