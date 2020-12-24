# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_xtext.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: xtext.py
AUTHOR: Igor Dejanovic
@summary: Lexer module for Xtext language.
          For more information see <http://www.eclipse.org/modeling/tmf/> or 
          <http://www.openarchitectureware.org/>.
"""
__author__ = 'Igor Dejanovic <igor.dejanovic@gmail.com>'
__svnid__ = '$Id: _xtext.py 70229 2012-01-01 01:27:10Z CJP $'
__revision__ = '$Revision: 70229 $'
import wx.stc as stc
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Token, Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
import re, synglob, syndata
(STC_XTEXT_DEFAULT, STC_XTEXT_COMMENT, STC_XTEXT_NUMBER, STC_XTEXT_STRING, STC_XTEXT_STRINGEOL, STC_XTEXT_OPERATOR, STC_XTEXT_NAME, STC_XTEXT_ABSTRACTRULE, STC_XTEXT_FEATURE, STC_XTEXT_CROSSREF, STC_XTEXT_PACKAGE, STC_XTEXT_KEYWORD, STC_XTEXT_KEYWORD_PSEUDO) = range(13)
KEYWORDS = 'grammar generate import returns enum terminal hidden with as current'
TERMINALS = 'ID INT STRING'
SYNTAX_ITEMS = [
 (
  STC_XTEXT_DEFAULT, 'default_style'),
 (
  STC_XTEXT_COMMENT, 'comment_style'),
 (
  STC_XTEXT_NUMBER, 'number_style'),
 (
  STC_XTEXT_STRING, 'string_style'),
 (
  STC_XTEXT_STRINGEOL, 'stringeol_style'),
 (
  STC_XTEXT_OPERATOR, 'operator_style'),
 (
  STC_XTEXT_NAME, 'default_style'),
 (
  STC_XTEXT_ABSTRACTRULE, 'keyword3_style'),
 (
  STC_XTEXT_FEATURE, 'default_style'),
 (
  STC_XTEXT_CROSSREF, 'class_style'),
 (
  STC_XTEXT_PACKAGE, 'class_style'),
 (
  STC_XTEXT_KEYWORD, 'keyword_style'),
 (
  STC_XTEXT_KEYWORD_PSEUDO, 'keyword2_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for XText"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CONTAINER)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, AutoIndenter)
        self.RegisterFeature(synglob.FEATURE_STYLETEXT, StyleText)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         (
          1, KEYWORDS)]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '//']


def StyleText(stc, start, end):
    """Style the text
    @param stc: Styled text control instance
    @param start: Start position
    @param end: end position

    """
    for (index, token, txt) in lexer.get_tokens_unprocessed(stc.GetTextRange(0, end)):
        style = TOKEN_MAP.get(token, STC_XTEXT_DEFAULT)
        stc.StartStyling(index, 31)
        tlen = len(txt)
        if tlen:
            stc.SetStyling(len(txt), style)


def AutoIndenter(estc, pos, ichar):
    """Auto indent xtext code.
    This code is based on python AutoIndenter.
    @param estc: EditraStyledTextCtrl
    @param pos: current carat position
    @param ichar: Indentation character
    @return: string

    """
    rtxt = ''
    line = estc.GetCurrentLine()
    spos = estc.PositionFromLine(line)
    text = estc.GetTextRange(spos, pos)
    eolch = estc.GetEOLChar()
    inspace = text.isspace()
    if inspace or not len(text):
        estc.AddText(eolch + text)
        return
    text = text.strip()
    if text.endswith(';'):
        estc.AddText(eolch)
        return
    indent = estc.GetLineIndentation(line)
    if ichar == '\t':
        tabw = estc.GetTabWidth()
    else:
        tabw = estc.GetIndent()
    i_space = indent / tabw
    end_spaces = (indent - tabw * i_space) * ' '
    if text.endswith(':'):
        i_space += 1
    rtxt = eolch + ichar * i_space + end_spaces
    estc.AddText(rtxt)


TOKEN_MAP = {Token.String: STC_XTEXT_STRING, Token.Comment.Multiline: STC_XTEXT_COMMENT, 
   Token.Comment.Single: STC_XTEXT_COMMENT, 
   Token.Operator: STC_XTEXT_OPERATOR, 
   Token.Punctuation: STC_XTEXT_OPERATOR, 
   Token.Number.Integer: STC_XTEXT_NUMBER, 
   Token.Keyword: STC_XTEXT_KEYWORD, 
   Token.Keyword.Pseudo: STC_XTEXT_KEYWORD_PSEUDO, 
   Token.Name: STC_XTEXT_NAME, 
   Token.Name.AbstractRule: STC_XTEXT_ABSTRACTRULE, 
   Token.Name.Feature: STC_XTEXT_FEATURE, 
   Token.Name.CrossRef: STC_XTEXT_CROSSREF, 
   Token.Name.Package: STC_XTEXT_PACKAGE, 
   Token.Name.Package.EMF: STC_XTEXT_PACKAGE}

class XTextLexer(RegexLexer):
    """
    Xtext lexer based on statefull RegexLexer from pygments library.
    """
    name = 'Xtext'
    aliases = ['xtext']
    filenames = ['*.xtxt']
    mimetypes = ['text/x-xtext']
    flags = re.MULTILINE | re.DOTALL

    def AltWords(words):
        """Makes lexer rule for alternative words from the given words list.
        @param words: string consisting of space separated words
        @return: string in the form \\bword1\\b|\\bword2\\b|\\bword3\x08...
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
                '/\\*', Comment.Multiline, 'comment'),
               (
                '\\n', Token.EndOfLine),
               (
                '//[^\\n]*$', Comment.Single),
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
                AltWords(KEYWORDS), Keyword),
               (
                AltWords(TERMINALS), Keyword.Pseudo),
               (
                _ident + '(::' + _ident + ')+', Name.Package.EMF)], 
       'parserrule': [
                    include('first'),
                    (
                     '(' + _ident + '(\\.' + _ident + ')?)([ \\t]*)(=|\\?=|\\+=)',
                     bygroups(Name.Feature, Text.Whitespace, Operator)),
                    (
                     _ident + '(\\.' + _ident + ')+', Name.Package),
                    (
                     _ident, Name.CrossRef),
                    (
                     ';', Punctuation, '#pop')], 
       'comment': [
                 (
                  '/\\*', Comment.Multiline, '#push'),
                 (
                  '\\*/', Comment.Multiline, '#pop'),
                 (
                  '\\n', Token.EndOfLine),
                 (
                  '[^/*\\n]+', Comment.Multiline),
                 (
                  '\\*|\\/', Comment.Multiline)]}


lexer = XTextLexer()
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