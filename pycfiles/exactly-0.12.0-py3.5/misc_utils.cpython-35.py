# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/section_document/element_parsers/misc_utils.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1872 bytes
import shlex
from exactly_lib.section_document.element_parsers.instruction_parser_exceptions import SingleInstructionInvalidArgumentException
from exactly_lib.section_document.element_parsers.token_stream import TokenStream, TokenSyntaxError
from exactly_lib.util.parse.token import Token

def new_token_stream(source: str) -> TokenStream:
    """
    Constructs a :class:`TokenStream`
    :rtype: :class:`TokenStream`
    :raises :class:`SingleInstructionInvalidArgumentException` Invalid syntax
    """
    try:
        return TokenStream(source)
    except TokenSyntaxError as ex:
        raise SingleInstructionInvalidArgumentException(std_error_message_text_for_token_syntax_error_from_exception(ex))


def std_error_message_text_for_token_syntax_error_from_exception(ex: TokenSyntaxError) -> str:
    return std_error_message_text_for_token_syntax_error(str(ex))


def std_error_message_text_for_token_syntax_error(syntax_error_message: str) -> str:
    return 'Invalid quoting of arguments: ' + syntax_error_message


def split_arguments_list_string(arguments: str) -> list:
    """
    :raises SingleInstructionInvalidArgumentException: The arguments string cannot be parsed.
    """
    try:
        return shlex.split(arguments)
    except ValueError as ex:
        raise SingleInstructionInvalidArgumentException('Invalid quoting of arguments: ' + str(ex))


def is_option_argument(argument: str) -> bool:
    return argument[0] == '-'


def is_option_token(token: Token) -> bool:
    return token.source_string[0] == '-'


def ensure_is_not_option_argument(argument: str):
    """
    :raises SingleInstructionInvalidArgumentException: The arguments is an option argument.
    """
    if is_option_argument(argument):
        raise SingleInstructionInvalidArgumentException('An option argument was not expected here: {}'.format(argument))