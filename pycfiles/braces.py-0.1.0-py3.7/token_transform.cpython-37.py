# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\braces\token_transform.py
# Compiled at: 2020-03-31 08:40:42
# Size of source mod 2**32: 2610 bytes
from collections import namedtuple
from io import StringIO
import tokenize
from .const import EXCEPT, INDENT, NEWLINE, TOKEN
__all__ = ('test_compile', 'transform', 'SmallToken')
SmallToken = namedtuple('SmallToken', 'type string')

def test_compile(code: str) -> None:
    compile(code, '<test>', 'exec')


def transform(code: str) -> str:
    tokens = list(tokenize.generate_tokens(StringIO(code).readline))
    result = [SmallToken(token.exact_type, token.string) for token in tokens]
    braces = []
    in_dict_or_set = False
    previous = None
    for token in tokens:
        if token.exact_type == TOKEN.LBRACE:
            if not previous or previous.exact_type in EXCEPT:
                in_dict_or_set = True
            else:
                braces.append(token)
        elif token.exact_type == TOKEN.RBRACE:
            if in_dict_or_set:
                in_dict_or_set = False
            else:
                braces.append(token)
        previous = token

    contexts = []
    for token in braces:
        if token.exact_type == TOKEN.LBRACE:
            contexts.append([tokens.index(token), None])
        else:
            for context in reversed(contexts):
                if context[1] is None:
                    context[1] = tokens.index(token)
                    break
            else:
                raise SyntaxError('Unmatched braces found.')

    offset = 0
    for indent, (start, end) in enumerate(contexts, 1):
        result[start + offset] = SmallToken(TOKEN.COLON, ':')
        offset += 1
        if result[(start + offset)].type in NEWLINE:
            offset -= 1
        else:
            result.insert(start + offset, SmallToken(TOKEN.NL, '\n'))
        result[end + offset] = SmallToken(TOKEN.DEDENT, '')
        offset += 1
        result.insert(start + offset, SmallToken(TOKEN.INDENT, INDENT * indent))

    offset = 0
    for index, token in enumerate(result.copy()):
        if token.string == ';':
            if result[(index - offset + 1)].type in NEWLINE:
                result.pop(index - offset)
                offset += 1
            else:
                result[index - offset] = (
                 TOKEN.NL, '\n')

    return tokenize.untokenize(result)