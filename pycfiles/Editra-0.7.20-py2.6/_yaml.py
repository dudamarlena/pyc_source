# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_yaml.py
# Compiled at: 2011-08-30 21:43:45
"""
FILE: yaml.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for YAML
@todo: Maybe new custom style for text regions

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _yaml.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx, wx.stc as stc, syndata
YAML_KW = [
 (0, 'true false yes no')]
SYNTAX_ITEMS = [
 (
  stc.STC_YAML_COMMENT, 'comment_style'),
 (
  stc.STC_YAML_DEFAULT, 'default_style'),
 (
  stc.STC_YAML_DOCUMENT, 'scalar_style'),
 (
  stc.STC_YAML_ERROR, 'error_style'),
 (
  stc.STC_YAML_IDENTIFIER, 'keyword2_style'),
 (
  stc.STC_YAML_KEYWORD, 'keyword_style'),
 (
  stc.STC_YAML_NUMBER, 'number_style'),
 (
  stc.STC_YAML_REFERENCE, 'global_style'),
 (
  stc.STC_YAML_TEXT, 'default_style')]
if wx.VERSION >= (2, 9, 0, 0, ''):
    SYNTAX_ITEMS.append((stc.STC_YAML_OPERATOR, 'operator_style'))
FOLD_COMMENT = ('fold.comment.yaml', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for YAML"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_YAML)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return YAML_KW

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD_COMMENT]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '#']