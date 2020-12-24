# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/parser/parse.py
# Compiled at: 2015-11-06 23:45:35
import salve
from salve.context import ExecutionContext
from salve.exceptions import ParsingException, BlockException
from salve.block import identifier
from salve.parser.tokenize import Token, tokenize_stream

def check_for_unexpected_token(token):
    """
    Checks the current token to see if it matches the currently expected types.
    If it doesn't, raise a ParsingException with a nicely formatted message.

    Args:
        @token
        The token to check against expected types
    """
    expected = ExecutionContext()['parsing']['expected_token_types']
    if token.ty not in expected:
        raise ParsingException('Invalid token.' + 'Expected a token of types ' + str(expected) + ' but got token ' + token.value + ' of type ' + token.ty + ' instead.', token.file_context)


def check_parsing_end_state():
    """
    Validates that the parsing state is a safe one for the parser to exit.
    For example, if we're in the middle of a block and the parser attempts to
    exit, this is an error condition and a ParsingException should be raised.
    """
    parsing_context = ExecutionContext()['parsing']
    if parsing_context['in_block'] or Token.types.TEMPLATE in parsing_context['expected_token_types']:
        raise ParsingException('Incomplete block in token stream!', parsing_context['current_block'].file_context)


def handle_token_noblock(token):
    """
    Handler for parsing a token outside of a block context. (i.e. not in curly
    braces)

    Looking either for an ID, a primary block attr, or a block start

    Args:
        @token
        The current token being parsed
    """
    parsing_context = ExecutionContext()['parsing']
    if token.ty == Token.types.IDENTIFIER:
        try:
            current_block = identifier.block_from_identifier(token)
            parsing_context['blocks'].append(current_block)
            parsing_context['current_block'] = current_block
        except BlockException:
            raise ParsingException('Invalid block id ' + token.value, token.file_context)

        parsing_context['expected_token_types'] = [Token.types.BLOCK_START, Token.types.TEMPLATE]
    elif token.ty == Token.types.BLOCK_START:
        parsing_context['in_block'] = True
        parsing_context['expected_token_types'] = [Token.types.BLOCK_END,
         Token.types.IDENTIFIER]
    elif token.ty == Token.types.TEMPLATE:
        parsing_context['expected_token_types'] = [
         Token.types.BLOCK_START,
         Token.types.IDENTIFIER]
        current_block = parsing_context['current_block']
        current_block[current_block.primary_attr] = token.value


def handle_token_in_block(token):
    """
    Handler for parsing a token inside of a block context. (i.e. in curly
    braces)
    Looks for a block attribute, an attribute value, or a block end.

    Args:
        @token
        The current token being parsed
    """
    parsing_context = ExecutionContext()['parsing']
    if token.ty == Token.types.BLOCK_END:
        parsing_context['in_block'] = False
        parsing_context['expected_token_types'] = [Token.types.IDENTIFIER]
    elif token.ty == Token.types.IDENTIFIER:
        parsing_context['current_attr'] = token.value.lower()
        parsing_context['expected_token_types'] = [Token.types.TEMPLATE]
    elif token.ty == Token.types.TEMPLATE:
        parsing_context['expected_token_types'] = [
         Token.types.BLOCK_END,
         Token.types.IDENTIFIER]
        parsing_context['current_block'][parsing_context['current_attr']] = token.value
        parsing_context['current_attr'] = None
    return


def handle_token(token):
    """
    Handles the parsing of a single token.
    Overall, takes the following two steps:
    - Check that the token is one of the expected types
    - Check if parsing is in the middle of building a block, and hand the token
      to the appropriate handler

    Args:
        @token
        The token from tokenization being parsed
    """
    check_for_unexpected_token(token)
    if not ExecutionContext()['parsing']['in_block']:
        handle_token_noblock(token)
    else:
        handle_token_in_block(token)


def parse_tokens(tokens):
    """
    Converts a token list to a block list.
    This is not entirely stateless, but unlike the tokenizer,
    there are no explicit states.

    Args:
        @tokens
        An iterable (generally a list) of Tokens to parse into Blocks.
        Unordered iterables won't work here, as parsing is very
        sensitive to token ordering.
    """
    salve.logger.info('Beginning Parse of Token Stream')
    ExecutionContext()['parsing'] = {}
    parsing_context = ExecutionContext()['parsing']
    parsing_context['blocks'] = []
    parsing_context['expected_token_types'] = [
     Token.types.IDENTIFIER]
    parsing_context['in_block'] = False
    parsing_context['current_block'] = None
    parsing_context['current_attr'] = None
    for token in tokens:
        handle_token(token)

    check_parsing_end_state()
    salve.logger.info('Finished Parsing Token Stream')
    return parsing_context['blocks']


def parse_stream(stream):
    """
    Parse a stream or file object into blocks.

    Args:
        @stream
        any file-like object that supports read() or readlines()
        Parsing a stream is just tokenizing it, and then handing those
        tokens to the parser.
    """
    return parse_tokens(tokenize_stream(stream))