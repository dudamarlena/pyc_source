# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scopedconfig/lexer.py
# Compiled at: 2019-03-17 14:14:39
import re
SYMBOL_OPTION = ':'
SYMBOL_SECTION_BEGIN = '{'
SYMBOL_SECTION_END = '}'
SYMBOL_WORD = ''

class Lexer(object):

    def __init__(self):
        self._tokens = []
        self._index = 0

    def tokenize(self, iterable):
        self._tokens = []
        self._index = 0
        for line in iterable:
            if line.lstrip() and line.lstrip()[0] == '#':
                continue
            tokens = re.findall('(?:[^\\s,"]|"(?:\\\\.|[^"])*")+', line)
            for (i, tok) in enumerate(tokens):
                if tok and tok.startswith('"') and tok.endswith('"'):
                    tokens[i] = tok[1:-1]

            if not tokens or not tokens[0] or tokens[0][0] == '#':
                continue
            for token in tokens:
                if token and token[(-1)] == SYMBOL_OPTION:
                    symbol = SYMBOL_OPTION
                    token = token[:-1]
                elif token == SYMBOL_SECTION_BEGIN:
                    symbol = SYMBOL_SECTION_BEGIN
                elif token == SYMBOL_SECTION_END:
                    symbol = SYMBOL_SECTION_END
                else:
                    symbol = SYMBOL_WORD
                self._tokens.append((token, symbol))

        self._index = 0
        return self

    def __iter__(self):
        if not self._tokens:
            return
        idx = -1
        while idx < len(self._tokens) - 1:
            idx += 1
            shift = yield self._tokens[idx]
            if shift:
                idx = idx - shift