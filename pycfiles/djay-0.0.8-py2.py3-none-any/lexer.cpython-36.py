# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/rply/rply/lexer.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 1689 bytes
from rply.errors import LexingError
from rply.token import SourcePosition, Token

class Lexer(object):

    def __init__(self, rules, ignore_rules):
        self.rules = rules
        self.ignore_rules = ignore_rules

    def lex(self, s):
        return LexerStream(self, s)


class LexerStream(object):

    def __init__(self, lexer, s):
        self.lexer = lexer
        self.s = s
        self.idx = 0
        self._lineno = 1

    def __iter__(self):
        return self

    def _update_pos(self, match):
        self.idx = match.end
        self._lineno += self.s.count('\n', match.start, match.end)
        last_nl = self.s.rfind('\n', 0, match.start)
        if last_nl < 0:
            return match.start + 1
        else:
            return match.start - last_nl

    def next(self):
        while True:
            if self.idx >= len(self.s):
                raise StopIteration
            for rule in self.lexer.ignore_rules:
                match = rule.matches(self.s, self.idx)
                if match:
                    self._update_pos(match)
                    break
            else:
                break

        for rule in self.lexer.rules:
            match = rule.matches(self.s, self.idx)
            if match:
                lineno = self._lineno
                colno = self._update_pos(match)
                source_pos = SourcePosition(match.start, lineno, colno)
                token = Token(rule.name, self.s[match.start:match.end], source_pos)
                return token
        else:
            raise LexingError(None, SourcePosition(self.idx, -1, -1))

    def __next__(self):
        return self.next()