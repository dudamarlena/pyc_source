# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_javascript.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: javascript.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for JavaScript.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _javascript.py 70228 2011-12-31 20:39:16Z CJP $'
__revision__ = '$Revision: 70228 $'
import wx.stc as stc, synglob, syndata, _cpp
JS_KEYWORDS = (0, 'abstract break boolean byte case const continue catch class char debugger default delete do double default export false else enum export extend final finally float for function goto if implements import in instanceof int interface long native new null package private protected public return short static synchronized switch super this throw throws transient try true typeof var void volatile with while')
SYNTAX_ITEMS = [
 (
  stc.STC_HJ_COMMENT, 'comment_style'),
 (
  stc.STC_HJ_COMMENTDOC, 'dockey_style'),
 (
  stc.STC_HJ_COMMENTLINE, 'comment_style'),
 (
  stc.STC_HJ_DEFAULT, 'default_style'),
 (
  stc.STC_HJ_DOUBLESTRING, 'string_style'),
 (
  stc.STC_HJ_KEYWORD, 'keyword_style'),
 (
  stc.STC_HJ_NUMBER, 'number_style'),
 (
  stc.STC_HJ_REGEX, 'scalar_style'),
 (
  stc.STC_HJ_SINGLESTRING, 'string_style'),
 (
  stc.STC_HJ_START, 'scalar_style'),
 (
  stc.STC_HJ_STRINGEOL, 'stringeol_style'),
 (
  stc.STC_HJ_SYMBOLS, 'array_style'),
 (
  stc.STC_HJ_WORD, 'class_style'),
 (
  stc.STC_HJA_COMMENT, 'comment_style'),
 (
  stc.STC_HJA_COMMENTDOC, 'dockey_style'),
 (
  stc.STC_HJA_COMMENTLINE, 'comment_style'),
 (
  stc.STC_HJA_DEFAULT, 'default_style'),
 (
  stc.STC_HJA_DOUBLESTRING, 'string_style'),
 (
  stc.STC_HJA_KEYWORD, 'keyword_style'),
 (
  stc.STC_HJA_NUMBER, 'number_style'),
 (
  stc.STC_HJA_REGEX, 'scalar_style'),
 (
  stc.STC_HJA_SINGLESTRING, 'string_style'),
 (
  stc.STC_HJA_START, 'scalar_style'),
 (
  stc.STC_HJA_STRINGEOL, 'stringeol_style'),
 (
  stc.STC_HJA_SYMBOLS, 'array_style'),
 (
  stc.STC_HJA_WORD, 'class_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for JavaScript"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, _cpp.AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         JS_KEYWORDS]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        if self.LangId == synglob.ID_LANG_HTML:
            return SYNTAX_ITEMS
        else:
            return _cpp.SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         ('fold', '1')]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '//']


def KeywordString(option=0):
    """Returns the specified Keyword String
    @keyword option: specific subset of keywords to get

    """
    return JS_KEYWORDS[1]