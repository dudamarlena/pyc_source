# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/element_parsers/token_parse.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 3652 bytes
import io, shlex
from exactly_lib.section_document.element_parsers.instruction_parser_exceptions import SingleInstructionInvalidArgumentException
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.util.parse.token import TokenType, Token

def parse_token_or_none_on_current_line(source: ParseSource, argument_description: str='argument') -> Token:
    """
    Parses a single, optional token from remaining part of current line.

    Tokens must be separated by space.

    :param source: Must have a current line. Initial space is consumed. Text for token is consumed.
    :raise SingleInstructionInvalidArgumentException: The token has invalid syntax
    """
    source.consume_initial_space_on_current_line()
    if source.is_at_eol:
        return
    part_of_current_line = source.remaining_part_of_current_line
    source_io = io.StringIO(part_of_current_line)
    lexer = shlex.shlex(source_io, posix=True)
    lexer.whitespace_split = True
    token_type = _derive_token_type(lexer, source.remaining_part_of_current_line[0])
    try:
        token_string = lexer.get_token()
    except ValueError as ex:
        msg = 'Invalid {}: {}'.format(argument_description, str(ex))
        raise SingleInstructionInvalidArgumentException(msg)

    source_string = _get_source_string_and_consume_token_characters(source, source_io)
    return Token(token_type, token_string, source_string)


def parse_token_on_current_line(source: ParseSource, argument_description: str='argument') -> Token:
    """
    Parses a single, mandatory token from remaining part of current line.

    Tokens must be separated by space.

    :param source: Must have a current line. Initial space is consumed. Text for token is consumed.
    :raise SingleInstructionInvalidArgumentException: There is no token
    :raise SingleInstructionInvalidArgumentException: The token has invalid syntax
    """
    token = parse_token_or_none_on_current_line(source, argument_description)
    if token is None:
        raise SingleInstructionInvalidArgumentException('Missing ' + argument_description)
    return token


def parse_plain_token_on_current_line(source: ParseSource, argument_description: str='argument') -> Token:
    """
    Parses a single, mandatory plain (unquoted) token from remaining part of current line.

    Tokens must be separated by space.

    :param source: Must have a current line. Initial space is consumed. Text for token is consumed.
    :raise SingleInstructionInvalidArgumentException: There is no token
    :raise SingleInstructionInvalidArgumentException: The token has invalid syntax
    """
    token = parse_token_on_current_line(source, argument_description)
    if token.type is TokenType.QUOTED:
        raise SingleInstructionInvalidArgumentException('Argument must not be quoted: ' + token.source_string)
    return token


def _derive_token_type(lexer: shlex.shlex, character: str) -> TokenType:
    if character in lexer.quotes:
        return TokenType.QUOTED
    return TokenType.PLAIN


def _get_source_string_and_consume_token_characters(source: ParseSource, source_io: io.StringIO) -> str:
    num_chars_consumed = source_io.tell()
    if source.remaining_part_of_current_line[(num_chars_consumed - 1)].isspace():
        num_chars_consumed -= 1
    ret_val = source.remaining_source[:num_chars_consumed]
    source.consume_part_of_current_line(num_chars_consumed)
    return ret_val