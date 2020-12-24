# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_make.py
# Compiled at: 2011-08-30 21:43:47
"""
FILE: make.py                                                               
AUTHOR: Cody Precord                                                        
@summary: Lexer configuration module for Makefiles.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _make.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, syndata
SYNTAX_ITEMS = [
 (
  stc.STC_MAKE_DEFAULT, 'default_style'),
 (
  stc.STC_MAKE_COMMENT, 'comment_style'),
 (
  stc.STC_MAKE_IDENTIFIER, 'scalar_style'),
 (
  stc.STC_MAKE_IDEOL, 'ideol_style'),
 (
  stc.STC_MAKE_OPERATOR, 'operator_style'),
 (
  stc.STC_MAKE_PREPROCESSOR, 'pre2_style'),
 (
  stc.STC_MAKE_TARGET, 'keyword_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Makefiles"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_MAKEFILE)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '#']