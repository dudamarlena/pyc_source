# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/ExcelFormulaLexer.py
# Compiled at: 2008-03-17 12:58:02
__rev_id__ = '$Id: ExcelFormulaLexer.py,v 1.4 2005/08/14 06:40:23 rvk Exp $'
import sys
from antlr import EOF, CommonToken as Tok, TokenStream, TokenStreamException
import struct, ExcelFormulaParser
from re import compile as recompile, match, LOCALE, UNICODE, IGNORECASE
int_const_pattern = recompile('\\d+')
flt_const_pattern = recompile('\\d*\\.\\d+(?:[Ee][+-]?\\d+)?')
str_const_pattern = recompile('["][^"]*["]')
ref2d_pattern = recompile('\\$?[A-I]?[A-Z]\\$?\\d+')
true_pattern = recompile('TRUE', IGNORECASE)
false_pattern = recompile('FALSE', IGNORECASE)
name_pattern = recompile('[\\.\\w]+', LOCALE)
pattern_type_tuples = (
 (
  flt_const_pattern, ExcelFormulaParser.NUM_CONST),
 (
  int_const_pattern, ExcelFormulaParser.INT_CONST),
 (
  str_const_pattern, ExcelFormulaParser.STR_CONST),
 (
  ref2d_pattern, ExcelFormulaParser.REF2D),
 (
  true_pattern, ExcelFormulaParser.TRUE_CONST),
 (
  false_pattern, ExcelFormulaParser.FALSE_CONST),
 (
  name_pattern, ExcelFormulaParser.NAME))
type_text_tuples = (
 (
  ExcelFormulaParser.NE, '<>'),
 (
  ExcelFormulaParser.LE, '<='),
 (
  ExcelFormulaParser.GE, '>='),
 (
  ExcelFormulaParser.EQ, '='),
 (
  ExcelFormulaParser.LT, '<'),
 (
  ExcelFormulaParser.GT, '>'),
 (
  ExcelFormulaParser.ADD, '+'),
 (
  ExcelFormulaParser.SUB, '-'),
 (
  ExcelFormulaParser.MUL, '*'),
 (
  ExcelFormulaParser.DIV, '/'),
 (
  ExcelFormulaParser.COLON, ':'),
 (
  ExcelFormulaParser.SEMICOLON, ';'),
 (
  ExcelFormulaParser.COMMA, ','),
 (
  ExcelFormulaParser.LP, '('),
 (
  ExcelFormulaParser.RP, ')'),
 (
  ExcelFormulaParser.CONCAT, '&'),
 (
  ExcelFormulaParser.PERCENT, '%'),
 (
  ExcelFormulaParser.POWER, '^'))

class Lexer(TokenStream):

    def __init__(self, text):
        self._text = text[:]
        self._pos = 0
        self._line = 0

    def isEOF(self):
        return len(self._text) <= self._pos

    def curr_ch(self):
        return self._text[self._pos]

    def next_ch(self, n=1):
        self._pos += n

    def is_whitespace(self):
        return self.curr_ch() in ' \t\n\r\x0c\x0b'

    def match_pattern(self, pattern, toktype):
        m = pattern.match(self._text[self._pos:])
        if m:
            start_pos = self._pos + m.start(0)
            end_pos = self._pos + m.end(0)
            tt = self._text[start_pos:end_pos]
            self._pos = end_pos
            return Tok(type=toktype, text=tt, col=start_pos + 1)
        else:
            return
            return

    def nextToken(self):
        while not self.isEOF() and self.is_whitespace():
            self.next_ch()

        if self.isEOF():
            return Tok(type=EOF)
        for ptt in pattern_type_tuples:
            t = self.match_pattern(*ptt)
            if t:
                return t

        for (ty, te) in type_text_tuples:
            if self.curr_ch() == te:
                self.next_ch()
                return Tok(type=ty, text=te, col=self._pos)

        raise TokenStreamException('Unknown char %s at %u col.' % (self.curr_ch(), self._pos))


if __name__ == '__main__':
    import locale
    locale.setlocale(locale.LC_ALL, 'russian')
    try:
        for t in Lexer(b'1+2+3+67.8678 + " @##$$$ klhkh kljhklhkl " + .58e-678*A1:B4 - 1lkjljlkjl3535\xef\xee\xf0\xef\xee\xf0'):
            print t

    except TokenStreamException, e:
        print 'error:', e