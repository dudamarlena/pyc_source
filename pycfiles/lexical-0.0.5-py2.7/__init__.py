# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lexical/__init__.py
# Compiled at: 2017-09-29 12:59:08
from __future__ import unicode_literals
from re import match
import re
from io import StringIO, BytesIO
import sys

class UnknownToken(Exception):
    """ Unknown token error when trying to tokenize a single line """

    def __init__(self, line, column, line_code):
        self.line_code = line_code
        self.line = line
        self.column = column
        super(UnknownToken, self).__init__(self.message)

    @property
    def message(self):
        msg = b'Unknown token @({line},{column}): {0}'
        return msg.format(self.line_code.rstrip(), **vars(self))


def is_string(code):
    return sys.version_info >= (3, 0) and type(code).__name__ == b'str' or type(code).__name__ == b'unicode'


def is_bytes(code):
    return sys.version_info >= (3, 0) and type(code).__name__ == b'bytes' or type(code).__name__ == b'str'


def code_line_generator(code):
    """ A generator for lines from a file/string, keeping the 
 at end """
    if is_string(code):
        stream = StringIO(code)
    else:
        if is_bytes(code):
            stream = BytesIO(code)
        else:
            stream = code
        while True:
            line = stream.readline()
            if line:
                yield line + b' '
            else:
                break


def analyse(code, token_types):
    for line, line_code in enumerate(code_line_generator(code), 1):
        column = 1
        while column <= len(line_code):
            remaining_line_code = line_code[column - 1:]
            for ttype in token_types:
                flags = ttype.get(b'flags', 0)
                m = match(ttype[b'regex'], remaining_line_code, re.S | flags)
                if m:
                    value = m.group(1)
                    if ttype[b'store']:
                        yield dict(type=ttype[b'type'], value=value, line=line, column=column)
                    column += len(value)
                    break
            else:
                raise UnknownToken(line, column, line_code)