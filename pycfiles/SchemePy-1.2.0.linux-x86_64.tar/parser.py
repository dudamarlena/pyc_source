# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/parser.py
# Compiled at: 2015-09-04 17:30:49
from __future__ import division
import re, cStringIO
from symbol import Symbol
from token import Token

class Parser(object):
    tokenizer = '\\s*(#`|#,@|#,|#\'|,@|[(\'`,)]|"(?:[\\\\].|;|[^\\\\"])*"|;.*|[^\\s(\'"`,;)]*)(.*)'
    eof_object = Symbol('#<eof-object>')
    eol_object = Symbol('#<eol-object>')

    @classmethod
    def stringParser(cls, string):
        return cls(cStringIO.StringIO(string))

    def __init__(self, _file):
        self.file = _file
        self.line = ''
        self.line_number = 0

    def gettokens(self):
        """Return the next token, reading new text into line buffer if needed."""
        while True:
            if self.line == '\n' or self.line == '':
                self.line = self.file.readline().decode('utf-8')
                self.line_number += 1
                if (self.line_number == 1 or self.line_number == 2) and self.line.startswith('#!'):
                    self.line = self.file.readline().decode('utf-8')
                    self.line_number += 1
            if self.line == '':
                break
            token, self.line = re.match(self.tokenizer, self.line).groups()
            if token != '' and not token.startswith(';'):
                yield Token(token).setLine(self.line_number)
            if self.line == '\n' or self.line == '':
                yield self.eol_object

        yield self.eof_object

    tokens = property(gettokens)

    def getast(self):
        tokens = self.gettokens()
        o = []
        for t in tokens:
            if t is self.eof_object:
                return o
            if t is self.eol_object:
                if o:
                    return o
                continue
            o.append(self.read_ahead(t, tokens))

    def read_ahead(self, token, tokens):
        if '(' == token:
            L = []
            while True:
                token = tokens.next()
                if token is self.eof_object:
                    raise SyntaxError('unexpected EOF in list')
                if token is self.eol_object:
                    continue
                if token == ')':
                    return L
                L.append(self.read_ahead(token, tokens))

        elif ')' == token:
            raise SyntaxError('unexpected )')
        elif token is self.eol_object:
            raise SyntaxError('unexpected eol')
        else:
            return token.symbol

    ast = property(getast)