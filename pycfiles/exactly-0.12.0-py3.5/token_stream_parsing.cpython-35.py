# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/element_parsers/token_stream_parsing.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1118 bytes
from typing import Iterable, Generic, Callable, TypeVar
from exactly_lib.section_document.element_parsers.token_stream_parser import ParserFromTokenParser, TokenParser
from exactly_lib.util.parse.token import TokenMatcher
PARSE_RESULT = TypeVar('PARSE_RESULT')

class TokenSyntaxSetup(Generic[PARSE_RESULT]):

    def __init__(self, matcher: TokenMatcher, parser_after_token: Callable[([TokenParser], PARSE_RESULT)]):
        self.matcher = matcher
        self.parser_after_token = parser_after_token


def parse_mandatory_choice_with_default(parser: TokenParser, syntax_element_name: str, choices: Iterable[TokenSyntaxSetup[PARSE_RESULT]], default: ParserFromTokenParser) -> PARSE_RESULT:
    parser.require_existing_valid_head_token(syntax_element_name)
    for syntax_setup in choices:
        if syntax_setup.matcher.matches(parser.head):
            parser.consume_head()
            return syntax_setup.parser_after_token(parser)

    return default(parser)