# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_django.py
# Compiled at: 2011-08-30 21:43:45
"""
FILE: django.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Django Templates.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _django.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
import synglob, syndata
(STC_DJANGO_DEFAULT, STC_DJANGO_COMMENT, STC_DJANGO_NUMBER, STC_DJANGO_STRING, STC_DJANGO_STRINGEOL, STC_DJANGO_SCALAR, STC_DJANGO_OPERATOR, STC_DJANGO_PREPROCESSOR, STC_DJANGO_ATTRIBUTE, STC_DJANGO_TAG, STC_DJANGO_BUILTIN, STC_DJANGO_KEYWORD) = range(12)
KEYWORDS = 'true false undefined null in as reversed recursive not and or is if else import with loop block forloop'
SYNTAX_ITEMS = [
 (
  STC_DJANGO_DEFAULT, 'default_style'),
 (
  STC_DJANGO_COMMENT, 'comment_style'),
 (
  STC_DJANGO_NUMBER, 'number_style'),
 (
  STC_DJANGO_STRING, 'string_style'),
 (
  STC_DJANGO_STRINGEOL, 'stringeol_style'),
 (
  STC_DJANGO_SCALAR, 'scalar_style'),
 (
  STC_DJANGO_OPERATOR, 'operator_style'),
 (
  STC_DJANGO_PREPROCESSOR, 'pre_style'),
 (
  STC_DJANGO_ATTRIBUTE, 'keyword2_style'),
 (
  STC_DJANGO_TAG, 'keyword_style'),
 (
  STC_DJANGO_BUILTIN, 'keyword4_style'),
 (
  STC_DJANGO_KEYWORD, 'keyword_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Django"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CONTAINER)
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
         '#']


def StyleText(stc, start, end):
    """Style the text
    @param stc: Styled text control instance
    @param start: Start position
    @param end: end position

    """
    cpos = 0
    stc.StartStyling(cpos, 31)
    lexer = get_lexer_by_name('html+django')
    doctxt = stc.GetTextRange(0, end)
    wineol = stc.GetEOLChar() == '\r\n'
    try:
        doctxt = doctxt.encode('utf-8')
    except:
        pass

    for (token, txt) in lexer.get_tokens(doctxt):
        style = TOKEN_MAP.get(token, STC_DJANGO_DEFAULT)
        if style == STC_DJANGO_PREPROCESSOR and txt.startswith('#'):
            style = STC_DJANGO_COMMENT
        tlen = len(txt)
        if wineol and '\n' in txt:
            tlen += txt.count('\n')
        if tlen:
            stc.SetStyling(tlen, style)
        cpos += tlen
        stc.StartStyling(cpos, 31)


TOKEN_MAP = {Token.Literal.String: STC_DJANGO_STRING, Token.Comment.Preproc: STC_DJANGO_PREPROCESSOR, 
   Token.Comment: STC_DJANGO_COMMENT, 
   Token.Name.Builtin: STC_DJANGO_BUILTIN, 
   Token.Operator: STC_DJANGO_OPERATOR, 
   Token.Punctuation: STC_DJANGO_OPERATOR, 
   Token.Number: STC_DJANGO_NUMBER, 
   Token.Keyword: STC_DJANGO_KEYWORD, 
   Token.Name.Attribute: STC_DJANGO_ATTRIBUTE, 
   Token.String.Interpol: STC_DJANGO_SCALAR, 
   Token.Name.Tag: STC_DJANGO_TAG}