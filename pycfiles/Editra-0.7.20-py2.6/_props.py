# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_props.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: props.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for properties/config files
          (ini, cfg, ect..).

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _props.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
SYNTAX_ITEMS = [
 (
  stc.STC_PROPS_ASSIGNMENT, 'operator_style'),
 (
  stc.STC_PROPS_COMMENT, 'comment_style'),
 (
  stc.STC_PROPS_DEFAULT, 'default_style'),
 (
  stc.STC_PROPS_DEFVAL, 'string_style'),
 (
  stc.STC_PROPS_KEY, 'scalar_style'),
 (
  stc.STC_PROPS_SECTION, 'keyword_style')]
FOLD = ('fold', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Properties files"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_PROPERTIES)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return list('#')