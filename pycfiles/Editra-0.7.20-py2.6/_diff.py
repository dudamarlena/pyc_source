# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_diff.py
# Compiled at: 2010-12-05 17:39:29
"""
FILE: diff.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Diff/Patch files

"""
__author__ = 'Cody Precord <cprecord@editra.org'
__svnid__ = '$Id: _diff.py 66108 2010-11-10 21:04:54Z CJP $'
__revision__ = '$Revision: 66108 $'
import wx, wx.stc as stc, synglob, syndata
SYNTAX_ITEMS = [
 (
  stc.STC_DIFF_ADDED, 'global_style'),
 (
  stc.STC_DIFF_COMMAND, 'pre_style'),
 (
  stc.STC_DIFF_COMMENT, 'comment_style'),
 (
  stc.STC_DIFF_DEFAULT, 'default_style'),
 (
  stc.STC_DIFF_DELETED, 'error_style'),
 (
  stc.STC_DIFF_HEADER, 'comment_style'),
 (
  stc.STC_DIFF_POSITION, 'pre_style')]
if wx.VERSION >= (2, 9, 0, 0, ''):
    SYNTAX_ITEMS.append((stc.STC_DIFF_CHANGED, 'default_style'))
FOLD = ('fold', '1')
FOLD_COMPACT = ('fold.compact', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Diff files"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_DIFF)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD, FOLD_COMPACT]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '--- ']