# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/tokenizer.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3961 bytes
import re
from .utils import BaronError

class UnknowItem(BaronError):
    pass


KEYWORDS = ('and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
            'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'nonlocal',
            'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise',
            'return', 'try', 'while', 'with', 'yield')
TOKENS = (('[a-zA-Z_]\\w*', 'NAME'), ('0', 'INT'), ('[-+]?\\d+[eE][-+]?\\d+[jJ]', 'FLOAT_EXPONANT_COMPLEX'),
          ('[-+]?\\d+.\\d?[eE][-+]?\\d+[jJ]', 'FLOAT_EXPONANT_COMPLEX'), ('[-+]?\\d?.\\d+[eE][-+]?\\d+[jJ]', 'FLOAT_EXPONANT_COMPLEX'),
          ('\\d+[eE][-+]?\\d*', 'FLOAT_EXPONANT'), ('\\d+\\.\\d*[eE][-+]?\\d*', 'FLOAT_EXPONANT'),
          ('\\.\\d+[eE][-+]?\\d*', 'FLOAT_EXPONANT'), ('\\d*\\.\\d+[jJ]', 'COMPLEX'),
          ('\\d+\\.[jJ]', 'COMPLEX'), ('\\d+[jJ]', 'COMPLEX'), ('\\d+\\.', 'FLOAT'),
          ('\\d*[_\\d]*\\.[_\\d]+[lL]?', 'FLOAT'), ('\\d+[_\\d]+\\.[_\\d]*[lL]?', 'FLOAT'),
          ('\\.', 'DOT'), ('[1-9]+[_\\d]*[lL]', 'LONG'), ('[1-9]+[_\\d]*', 'INT'),
          ('0[xX][\\d_a-fA-F]+[lL]?', 'HEXA'), ('(0[oO][0-7]+)|(0[0-7_]*)[lL]?', 'OCTA'),
          ('0[bB][01_]+[lL]?', 'BINARY'), ('\\(', 'LEFT_PARENTHESIS'), ('\\)', 'RIGHT_PARENTHESIS'),
          (':', 'COLON'), (',', 'COMMA'), (';', 'SEMICOLON'), ('@', 'AT'), ('\\+', 'PLUS'),
          ('-', 'MINUS'), ('\\*', 'STAR'), ('/', 'SLASH'), ('\\|', 'VBAR'), ('&', 'AMPER'),
          ('@', 'AT'), ('<', 'LESS'), ('>', 'GREATER'), ('=', 'EQUAL'), ('%', 'PERCENT'),
          ('\\[', 'LEFT_SQUARE_BRACKET'), ('\\]', 'RIGHT_SQUARE_BRACKET'), ('\\{', 'LEFT_BRACKET'),
          ('\\}', 'RIGHT_BRACKET'), ('`', 'BACKQUOTE'), ('==', 'EQUAL_EQUAL'), ('<>', 'NOT_EQUAL'),
          ('!=', 'NOT_EQUAL'), ('<=', 'LESS_EQUAL'), ('>=', 'GREATER_EQUAL'), ('~', 'TILDE'),
          ('\\^', 'CIRCUMFLEX'), ('<<', 'LEFT_SHIFT'), ('>>', 'RIGHT_SHIFT'), ('\\*\\*', 'DOUBLE_STAR'),
          ('\\+=', 'PLUS_EQUAL'), ('-=', 'MINUS_EQUAL'), ('@=', 'AT_EQUAL'), ('\\*=', 'STAR_EQUAL'),
          ('/=', 'SLASH_EQUAL'), ('%=', 'PERCENT_EQUAL'), ('&=', 'AMPER_EQUAL'),
          ('\\|=', 'VBAR_EQUAL'), ('\\^=', 'CIRCUMFLEX_EQUAL'), ('<<=', 'LEFT_SHIFT_EQUAL'),
          ('>>=', 'RIGHT_SHIFT_EQUAL'), ('\\.\\.\\.', 'ELLIPSIS'), ('->', 'RIGHT_ARROW'),
          ('\\*\\*=', 'DOUBLE_STAR_EQUAL'), ('//', 'DOUBLE_SLASH'), ('//=', 'DOUBLE_SLASH_EQUAL'),
          ('\\n', 'ENDL'), ('\\r\\n', 'ENDL'), ('#.*', 'COMMENT'), ('(\\s|\\\\\\n|\\\\\\r\\n)+', 'SPACE'),
          ('["\\\'](.|\\n|\\r)*["\\\']', 'STRING'), ('[uU]["\\\'](.|\\n|\\r)*["\\\']', 'UNICODE_STRING'),
          ('[fF]["\\\'](.|\\n|\\r)*["\\\']', 'INTERPOLATED_STRING'), ('[rR]["\\\'](.|\\n|\\r)*["\\\']', 'RAW_STRING'),
          ('[bB]["\\\'](.|\\n|\\r)*["\\\']', 'BINARY_STRING'), ('[uU][rR]["\\\'](.|\\n|\\r)*["\\\']', 'UNICODE_RAW_STRING'),
          ('[bB][rR]["\\\'](.|\\n|\\r)*["\\\']', 'BINARY_RAW_STRING'), ('[fF][rR]["\\\'](.|\\n|\\r)*["\\\']', 'INTERPOLATED_RAW_STRING'),
          ('[rR][fF]["\\\'](.|\\n|\\r)*["\\\']', 'INTERPOLATED_RAW_STRING'))
TOKENS = [(re.compile('^' + x[0] + '$'), x[1]) for x in TOKENS]

def tokenize(sequence, print_function=False):
    return list(tokenize_generator(sequence, print_function))


def tokenize_current_keywords(print_function=False):
    if print_function is True:
        return [x for x in KEYWORDS if x not in ('print', 'exec')]
    else:
        return KEYWORDS


def tokenize_generator(sequence, print_function=False):
    current_keywords = tokenize_current_keywords()
    for item in sequence:
        if item in current_keywords:
            yield (
             item.upper(), item)
        else:
            for candidate, token_name in TOKENS:
                if candidate.match(item):
                    yield (
                     token_name, item)
                    break
            else:
                raise UnknowItem("Can't find a matching token for this item: '%s'" % item)

    yield ('ENDMARKER', '')
    yield