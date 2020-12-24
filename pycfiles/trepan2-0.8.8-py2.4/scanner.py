# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/parse/scanner.py
# Compiled at: 2018-10-27 14:00:27
"""
Simple SPARK-style scanner
Copyright (c) 2017-2018 Rocky Bernstein
"""
import re
from spark_parser.scanner import GenericScanner
from trepan.processor.parse.tok import Token

class ScannerError(Exception):
    __module__ = __name__

    def __init__(self, text, text_cursor):
        self.text = text
        self.text_cursor = text_cursor

    def __str__(self):
        return self.text + '\n' + self.text_cursor


class LocationScanner(GenericScanner):
    __module__ = __name__

    def error(self, s):
        """Show text and a caret under that. For example:
x = 2y + z
     ^
"""
        raise ScannerError('%s' % s, '%s^' % (' ' * (self.pos - 1)))

    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv

    def add_token(self, name, v):
        t = Token(kind=name, value=v, offset=self.pos)
        self.pos += len(str(v))
        self.rv.append(t)

    def t_whitespace(self, s):
        r"""\s+"""
        self.add_token('SPACE', s)
        self.pos += len(s)

    def t_file_or_func(self, s):
        r'''(?:[^*-+,\d\'"\t \n:][^\'"\t \n:,]*)|(?:^""".+""")|(?:\'\'\'.+\'\'\')'''
        maybe_funcname = True
        if s == 'if':
            self.add_token('IF', s)
            return
        if s[0] in frozenset(('"', "'")):
            if s.startswith("'''") and s.endswith("'''") or s.startswith('"""') and s.endswith('"""'):
                base = s[3:-3]
            else:
                base = s[1:-1]
            maybe_funcname = False
        else:
            base = s
        if maybe_funcname and re.match('[a-zA-Z_][[a-zA-Z_.0-9\\[\\]]+\\(\\)', s):
            self.add_token('FUNCNAME', base)
        else:
            self.add_token('FILENAME', base)
        self.pos += len(s)

    def t_single_quote_file(self, s):
        """'[^'].+'"""
        base = s[1:-1]
        self.add_token('FILENAME', base)
        self.pos += len(s)

    def t_double_quote_file(self, s):
        """"[^"]+\""""
        base = s[1:-1]
        self.add_token('FILENAME', base)
        self.pos += len(s)

    def t_colon(self, s):
        """:"""
        self.add_token('COLON', s)
        self.pos += len(s)

    def t_comma(self, s):
        ""","""
        self.add_token('COMMA', s)
        self.pos += len(s)

    def t_direction(self, s):
        """^[+-]$"""
        self.add_token('DIRECTION', s)
        self.pos += len(s)

    def t_number(self, s):
        r"""\d+"""
        pos = self.pos
        self.add_token('NUMBER', int(s))
        self.pos = pos + len(s)

    def t_offset(self, s):
        r"""[+]\d+"""
        pos = self.pos
        self.add_token('OFFSET', s)
        self.pos = pos + len(s)

    def t_address(self, s):
        r"""[*]\d+"""
        pos = self.pos
        self.add_token('ADDRESS', s)
        self.pos = pos + len(s)


if __name__ == '__main__':
    for line in ("'/tmp/foo.py:12'", '6', '*6'):
        try:
            tokens = LocationScanner().tokenize(line.strip())
            for t in tokens:
                print t

        except ScannerError, e:
            print 'Lexical error at or around: '
            print e.text
            print e.text_cursor