# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_ada.py
# Compiled at: 2011-08-30 21:43:47
"""
 FILE: ada.py
 AUTHOR: Cody Precord
 @summary: Lexer configuration module for ada
 @todo: styles, keywords, testing

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _ada.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
ADA_KEYWORDS = (0, 'abort abstract accept access aliased all array at begin body case constant declare delay delta digits do else elsif end entry exception exit for function generic goto if in is limited loop new null of others out package pragma private procedure protected raise range record renames requeue return reverse select separate subtype tagged task terminate then type until use when while with')
SYNTAX_ITEMS = [
 (
  stc.STC_ADA_CHARACTER, 'char_style'),
 (
  stc.STC_ADA_CHARACTEREOL, 'stringeol_style'),
 (
  stc.STC_ADA_COMMENTLINE, 'comment_style'),
 (
  stc.STC_ADA_DEFAULT, 'default_style'),
 (
  stc.STC_ADA_DELIMITER, 'operator_style'),
 (
  stc.STC_ADA_IDENTIFIER, 'default_style'),
 (
  stc.STC_ADA_ILLEGAL, 'error_style'),
 (
  stc.STC_ADA_LABEL, 'keyword2_style'),
 (
  stc.STC_ADA_NUMBER, 'number_style'),
 (
  stc.STC_ADA_STRING, 'string_style'),
 (
  stc.STC_ADA_STRINGEOL, 'stringeol_style'),
 (
  stc.STC_ADA_WORD, 'keyword_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Ada"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_ADA)

    def GetKeywords(self):
        """Returns Specified Keywords List"""
        return [
         ADA_KEYWORDS]

    def GetSyntaxSpec(self):
        """Syntax Specifications"""
        return SYNTAX_ITEMS

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code"""
        return [
         '--']