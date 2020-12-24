# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_editra_ss.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: editra_ss.py                                                          
AUTHOR: Cody Precord                                                        
@summary: Lexer configuration file for Editra Syntax Highlighter Style Sheets.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _editra_ss.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
from _css import AutoIndenter
ESS_KEYWORDS = (0, 'fore back face size eol bold italic modifiers')
SYNTAX_ITEMS = [
 (
  stc.STC_CSS_DEFAULT, 'default_style'),
 (
  stc.STC_CSS_CLASS, 'global_style'),
 (
  stc.STC_CSS_COMMENT, 'comment_style'),
 (
  stc.STC_CSS_DIRECTIVE, 'directive_style'),
 (
  stc.STC_CSS_DOUBLESTRING, 'string_style'),
 (
  stc.STC_CSS_ID, 'scalar_style'),
 (
  stc.STC_CSS_IDENTIFIER, 'keyword4_style'),
 (
  stc.STC_CSS_IDENTIFIER2, 'keyword3_style'),
 (
  stc.STC_CSS_IMPORTANT, 'error_style'),
 (
  stc.STC_CSS_OPERATOR, 'operator_style'),
 (
  stc.STC_CSS_PSEUDOCLASS, 'scalar_style'),
 (
  stc.STC_CSS_SINGLESTRING, 'string_style'),
 (
  stc.STC_CSS_TAG, 'keyword_style'),
 (
  stc.STC_CSS_UNKNOWN_IDENTIFIER, 'unknown_style'),
 (
  stc.STC_CSS_UNKNOWN_PSEUDOCLASS, 'unknown_style'),
 (
  stc.STC_CSS_VALUE, 'char_style')]
FOLD = ('fold', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Editra Style Sheets"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CSS)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         ESS_KEYWORDS]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '/*', '*/']