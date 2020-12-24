# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_latex.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: latex.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Tex/LaTex.
@todo: Fairly poor needs lots of work.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _latex.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
TEX_KW = (0, 'Downarrow backslash lceil rceil Uparrow downarrow lfloor rfloor Updownarrow langle rangle Vert')
DUTCH = (1, '')
ENG = (2, '')
GERMAN = (3, '')
CZECH = (4, '')
ITALIAN = (5, '')
ROMAINIAN = (6, '')
SYNTAX_ITEMS1 = [
 (
  stc.STC_TEX_DEFAULT, 'default_style'),
 (
  stc.STC_TEX_COMMAND, 'keyword_style'),
 (
  stc.STC_TEX_GROUP, 'scalar_style'),
 (
  stc.STC_TEX_SPECIAL, 'operator_style'),
 (
  stc.STC_TEX_SYMBOL, 'number_style'),
 (
  stc.STC_TEX_TEXT, 'default_style')]
SYNTAX_ITEMS2 = [
 (
  stc.STC_L_DEFAULT, 'default_style'),
 (
  stc.STC_L_COMMAND, 'pre_style'),
 (
  stc.STC_L_COMMENT, 'comment_style'),
 (
  stc.STC_L_MATH, 'operator_style'),
 (
  stc.STC_L_TAG, 'keyword_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for LaTeX/TeX"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        if self.LangId == synglob.ID_LANG_LATEX:
            self.SetLexer(stc.STC_LEX_LATEX)
        else:
            self.SetLexer(stc.STC_LEX_TEX)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         TEX_KW]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        if self.LangId == synglob.ID_LANG_TEX:
            return SYNTAX_ITEMS1
        else:
            return SYNTAX_ITEMS2

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '%']