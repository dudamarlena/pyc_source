# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_nonmem.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: nonmem.py
AUTHOR: Cody Precord, Torsten Mohr, Robert McLeay
@summary: Lexer configuration module for NONMEM control streams.

"""
__author__ = 'Cody Precord <cprecord>, Torsten Mohr <none_yet>'
__svnid__ = '$Id: _nonmem.py 70229 2012-01-01 01:27:10Z CJP $'
__revision__ = '$Revision: 70229 $'
import wx.stc as stc
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Token, Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
import re, synglob, syndata
(STC_NONMEM_DEFAULT, STC_NONMEM_COMMENT, STC_NONMEM_NUMBER, STC_NONMEM_STRING, STC_NONMEM_STRINGEOL, STC_NONMEM_OPERATOR, STC_NONMEM_NAME, STC_NONMEM_ABSTRACTRULE, STC_NONMEM_FEATURE, STC_NONMEM_CROSSREF, STC_NONMEM_PACKAGE, STC_NONMEM_KEYWORD, STC_NONMEM_KEYWORD_PSEUDO) = range(13)
KEYWORDS = 'grammar generate import returns enum terminal hidden with as current'
TERMINALS = 'ID INT STRING'
SYNTAX_ITEMS = [
 (
  STC_NONMEM_DEFAULT, 'default_style'),
 (
  STC_NONMEM_COMMENT, 'comment_style'),
 (
  STC_NONMEM_NUMBER, 'number_style'),
 (
  STC_NONMEM_STRING, 'string_style'),
 (
  STC_NONMEM_STRINGEOL, 'stringeol_style'),
 (
  STC_NONMEM_OPERATOR, 'operator_style'),
 (
  STC_NONMEM_NAME, 'default_style'),
 (
  STC_NONMEM_ABSTRACTRULE, 'keyword3_style'),
 (
  STC_NONMEM_FEATURE, 'default_style'),
 (
  STC_NONMEM_CROSSREF, 'class_style'),
 (
  STC_NONMEM_PACKAGE, 'class_style'),
 (
  STC_NONMEM_KEYWORD, 'keyword_style'),
 (
  STC_NONMEM_KEYWORD_PSEUDO, 'keyword2_style')]
NONMEM_KEYWORDS = 'ADVAN\\d+ BLOCK COMP COND CONDITIONAL DEFDOSE DEFOBS DOWHILE ELSE ENDDO ENDIF EXP FILE FIX FIXED ICALL IF IGNORE INTER INTERACTION LOG MATRIX MAX MAXEVAL METHOD NEWIND NOABORT NOAPPEND NOPRINT NOHEADER ONEHEADER PRINT SIG SIGDIGITS SLOW SUBPROBLEMS THEN TOL TRANS1 TRANS2 TRANS3 TRANS4 ONLYSIM ENDIF'
NONMEM_PARAMS = 'DADT ERR EPS ETA THETA'

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for IssueLists
    This class is primarily intended as an example to creating a custom
    lexer.

    """

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CONTAINER)
        self.RegisterFeature(synglob.FEATURE_STYLETEXT, StyleText)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS


def StyleText(_stc, start, end):
    """Style the text
    @param _stc: Styled text control instance
    @param start: Start position
    @param end: end position

    """
    for (index, token, txt) in lexer.get_tokens_unprocessed(_stc.GetTextRange(0, end)):
        style = TOKEN_MAP.get(token, STC_NONMEM_DEFAULT)
        _stc.StartStyling(index, 31)
        tlen = len(txt)
        if tlen:
            _stc.SetStyling(len(txt), style)


TOKEN_MAP = {Token.String: STC_NONMEM_STRING, Token.Comment.Multiline: STC_NONMEM_COMMENT, Token.Comment.Single: STC_NONMEM_COMMENT, 
   Token.Operator: STC_NONMEM_OPERATOR, 
   Token.Punctuation: STC_NONMEM_OPERATOR, 
   Token.Number.Integer: STC_NONMEM_NUMBER, 
   Token.Keyword: STC_NONMEM_KEYWORD, 
   Token.Keyword.Pseudo: STC_NONMEM_KEYWORD_PSEUDO, 
   Token.Name: STC_NONMEM_NAME, 
   Token.Name.AbstractRule: STC_NONMEM_ABSTRACTRULE, 
   Token.Name.Feature: STC_NONMEM_FEATURE, 
   Token.Name.CrossRef: STC_NONMEM_CROSSREF, 
   Token.Name.Package: STC_NONMEM_PACKAGE, 
   Token.Name.Package.EMF: STC_NONMEM_PACKAGE}

class NONMEMLexer(RegexLexer):
    """
    Nonmem lexer based on statefull RegexLexer from pygments library.
    """
    name = 'NONMEM'
    aliases = ['nonmem']
    filenames = ['*.ctl']
    mimetypes = ['text/x-nonmem']
    flags = re.MULTILINE | re.DOTALL

    def AltWords(words):
        r"""Makes lexer rule for alternative words from the given words list.
        @param words: string consisting of space separated words
        @return: string in the form \bword1\b|\bword2\b|\bword3\b...
        """
        return ('|').join([ '\\b%s\\b' % w for w in words.split() ])

    _ident = '\\^?[a-zA-Z_\\$][a-zA-Z0-9_]*'
    tokens = {'root': [
              include('first'),
              (
               _ident + '(\\.' + _ident + ')+', Name.Package),
              (
               '(' + _ident + ')(\\s*)(returns)',
               bygroups(Name.AbstractRule, Text.Whitespace, Keyword), 'parserrule'),
              (
               '(' + _ident + ')(\\s*)(:)',
               bygroups(Name.AbstractRule, Text.Whitespace, Punctuation), 'parserrule'),
              (
               _ident, Name)], 
       'first': [
               (
                ';[^\\n]*$', Comment.Single),
               (
                '\\$[A-Z]+', Name.Package),
               (
                '[ \\t]+', Text.Whitespace),
               (
                '"(\\\\\\\\|\\\\"|[^"])*"', String),
               (
                "'(\\\\\\\\|\\\\'|[^'])*'", String),
               (
                '\\*|\\?|\\+|!|\\||=|\\?=|\\+=|\\.\\.|->', Operator),
               (
                '[()\\[\\]{}:]', Punctuation),
               (
                '[0-9]+', Number.Integer),
               (
                AltWords(NONMEM_KEYWORDS), Keyword),
               (
                AltWords(NONMEM_PARAMS), Keyword.Pseudo)], 
       'parserrule': [
                    include('first'),
                    (
                     '(' + _ident + '(\\.' + _ident + ')?)([ \\t]*)(=|\\?=|\\+=)',
                     bygroups(Name.Feature, Text.Whitespace, Operator)),
                    (
                     _ident + '(\\.' + _ident + ')+', Name.Package),
                    (
                     _ident, Name.CrossRef)]}


lexer = NONMEMLexer()
if __name__ == '__main__':
    import codecs, sys
    ftext = codecs.open(sys.argv[1], 'r', 'utf-8')
    text = ftext.read()
    ftext.close()
    line = 1
    for (index, token, txt) in lexer.get_tokens_unprocessed(text):
        if token is Token.EndOfLine:
            line += 1
        print line, token, txt