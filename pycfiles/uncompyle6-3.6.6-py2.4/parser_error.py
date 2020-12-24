# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/semantics/parser_error.py
# Compiled at: 2020-04-18 17:55:36
import uncompyle6.parser as python_parser

class ParserError(python_parser.ParserError):
    __module__ = __name__

    def __init__(self, error, tokens, debug):
        self.error = error
        self.tokens = tokens
        self.debug = debug

    def __str__(self):
        lines = [
         '--- This code section failed: ---']
        if self.debug:
            lines.extend([ t.format(token_num=i + 1) for (i, t) in enumerate(self.tokens) ])
        else:
            lines.extend([ t.format() for t in self.tokens ])
        lines.extend(['', str(self.error)])
        return ('\n').join(lines)