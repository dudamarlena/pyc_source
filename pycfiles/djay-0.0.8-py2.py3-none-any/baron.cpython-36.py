# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/baron.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 3245 bytes
from .spliter import split
from .grouper import group
from .tokenizer import tokenize as _tokenize
from .formatting_grouper import group as space_group
from .future import has_print_function, replace_print_by_name
from .grammator import generate_parse
from .indentation_marker import mark_indentation
from .inner_formatting_grouper import group as inner_group
from .parser import ParsingError
parse_tokens = generate_parse(False)
parse_tokens_print_function = generate_parse(True)

def _parse(tokens, print_function):
    parser = parse_tokens if not print_function else parse_tokens_print_function
    try:
        try:
            return parser(tokens)
        except ParsingError:
            parser = parse_tokens if print_function else parse_tokens_print_function
            return parser(tokens)

    except ParsingError as e:
        raise
    except Exception as e:
        import sys, traceback
        traceback.print_exc(file=(sys.stderr))
        sys.stderr.write('%s\n' % e)
        sys.stderr.write('\nBaron has failed to parse this input. If this is valid python code (and by that I mean that the python binary successfully parse this code without any syntax error) (also consider that python does not yet parse python 3 code integrally) it would be kind if you can extract a snippet of your code that make Baron fails and open a bug here: https://github.com/PyCQA/baron/issues\n\nSorry for the inconvenience.')


def parse(source_code, print_function=None):
    newline_appended = False
    linesep = '\r\n' if source_code.endswith('\r\n') else '\n'
    if source_code:
        if not source_code.endswith(linesep):
            source_code += linesep
            newline_appended = True
    else:
        if print_function is None:
            tokens = tokenize(source_code, False)
            print_function = has_print_function(tokens)
            if print_function:
                replace_print_by_name(tokens)
        else:
            tokens = tokenize(source_code, print_function)
    if newline_appended:
        to_return = _parse(tokens, print_function)
        if to_return[(-1)]['type'] == 'endl':
            if not to_return[(-1)]['formatting']:
                return to_return[:-1]
        if to_return[(-1)]['type'] == 'endl':
            if to_return[(-1)]['formatting']:
                return to_return[:-1] + to_return[(-1)]['formatting']
        return to_return
    else:
        return _parse(tokens, print_function)


def tokenize(pouet, print_function=False):
    splitted = split(pouet)
    grouped = group(splitted)
    print_tokenized = _tokenize(grouped, print_function)
    space_grouped = space_group(print_tokenized)
    inner_grouped = inner_group(space_grouped)
    indentation_marked = mark_indentation(inner_grouped)
    return indentation_marked