# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pylox/scanner.py
# Compiled at: 2017-01-19 18:15:08
# Size of source mod 2**32: 5185 bytes
import string
from .token import Token
from .tokentype import TokenType

class Scanner(object):

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self.keywords = {'and':TokenType.AND, 
         'class':TokenType.CLASS, 
         'else':TokenType.ELSE, 
         'false':TokenType.FALSE, 
         'for':TokenType.FOR, 
         'fun':TokenType.FUN, 
         'if':TokenType.IF, 
         'nil':TokenType.NIL, 
         'or':TokenType.OR, 
         'print':TokenType.PRINT, 
         'return':TokenType.RETURN, 
         'super':TokenType.SUPER, 
         'this':TokenType.THIS, 
         'true':TokenType.TRUE, 
         'var':TokenType.VAR, 
         'while':TokenType.WHILE}

    def _is_at_end(self):
        return self._current >= len(self.source)

    def scan_tokens(self):
        while not self._is_at_end():
            self._start = self._current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self._line))
        return self.tokens

    def scan_token(self):
        c = self._advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        else:
            if c == ')':
                self.add_token(TokenType.RIGHT_PAREN)
            else:
                if c == '{':
                    self.add_token(TokenType.LEFT_BRACE)
                else:
                    if c == '}':
                        self.add_token(TokenType.RIGHT_BRACE)
                    else:
                        if c == ',':
                            self.add_token(TokenType.COMMA)
                        else:
                            if c == '.':
                                self.add_token(TokenType.DOT)
                            else:
                                if c == '-':
                                    self.add_token(TokenType.MINUS)
                                else:
                                    if c == '+':
                                        self.add_token(TokenType.PLUS)
                                    else:
                                        if c == ';':
                                            self.add_token(TokenType.SEMICOLON)
                                        else:
                                            if c == '*':
                                                self.add_token(TokenType.STAR)
                                            else:
                                                if c == '!':
                                                    self.add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
                                                else:
                                                    if c == '=':
                                                        self.add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
                                                    else:
                                                        if c == '<':
                                                            self.add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
                                                        else:
                                                            if c == '>':
                                                                self.add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
                                                            else:
                                                                if c == '/':
                                                                    if self._match('/'):
                                                                        while self._peek() != '\n' and not self._is_at_end():
                                                                            self._advance()

                                                                    else:
                                                                        self.add_token(TokenType.SLASH)
                                                                else:
                                                                    if c in (' ', '\r',
                                                                             '\t'):
                                                                        pass
                                                                    else:
                                                                        if c == '\n':
                                                                            self._line += 1
                                                                        else:
                                                                            if c == '"':
                                                                                self.string()
                                                                            else:
                                                                                if self._is_digit(c):
                                                                                    self.number()
                                                                                else:
                                                                                    if self._is_alpha(c):
                                                                                        self.identifier()
                                                                                    else:
                                                                                        Lox().error(line, 'Unexpected character.')

    def identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()

        text = self.source[self._start:self._current]
        token_type = self.keywords.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        self.add_token(token_type)

    def number(self):
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == '.':
            if self._is_digit(self._peek_next()):
                self._advance()
                while self._is_digit(self._peek()):
                    self._advance()

        self.add_token(TokenType.NUMBER, float(self.source[self._start:self._current]))

    def string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek == '\n':
                self._line += 1
            self._advance()

        if self._is_at_end():
            Lox().error(line, 'Unterminated string.')
        self._advance()
        value = self.source[self._start + 1:self._current - 1]
        self.add_token(TokenType.STRING, value)

    def _is_digit(self, c):
        return '0' <= c <= '9'

    def _is_alpha(self, c):
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def _is_alpha_numeric(self, c):
        return self._is_alpha(c) or self._is_digit(c)

    def _match(self, expected):
        if self._is_at_end():
            return False
        else:
            if self.source[self._current] != expected:
                return False
            self._current += 1
            return True

    def _peek(self):
        if self._current >= len(self.source):
            return '\x00'
        else:
            return self.source[self._current]

    def _peek_next(self):
        if self._current + 1 >= len(self.source):
            return '\x00'
        else:
            return self.source[(self._current + 1)]

    def _advance(self):
        self._current += 1
        return self.source[(self._current - 1)]

    def add_token(self, token_type, literal=None):
        text = self.source[self._start:self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))