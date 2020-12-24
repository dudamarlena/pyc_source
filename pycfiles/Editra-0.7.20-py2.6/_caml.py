# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_caml.py
# Compiled at: 2010-12-05 17:39:29
"""
FILE: caml.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Caml

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _caml.py 66108 2010-11-10 21:04:54Z CJP $'
__revision__ = '$Revision: 66108 $'
import wx, wx.stc as stc, synglob, syndata
CAML_KW1 = (0, 'and as assert asr begin class constraint do done downto else end exception external false for fun function functor if in include inherit initializer land lazy let lor lsl lsr lxor match method mod module mutable new object of open or private rec sig struct then to true try type val virtual when while with')
CAML_KW2 = (1, 'option Some None ignore ref lnot succ pred parser')
CAML_KW3 = (2, 'array bool char float int list string unit')
SYNTAX_ITEMS = [
 (
  stc.STC_CAML_CHAR, 'char_style'),
 (
  stc.STC_CAML_COMMENT, 'comment_style'),
 (
  stc.STC_CAML_COMMENT1, 'comment_style'),
 (
  stc.STC_CAML_COMMENT2, 'comment_style'),
 (
  stc.STC_CAML_COMMENT3, 'comment_style'),
 (
  stc.STC_CAML_DEFAULT, 'default_style'),
 (
  stc.STC_CAML_IDENTIFIER, 'default_style'),
 (
  stc.STC_CAML_KEYWORD, 'keyword_style'),
 (
  stc.STC_CAML_KEYWORD2, 'pre_style'),
 (
  stc.STC_CAML_KEYWORD3, 'keyword2_style'),
 (
  stc.STC_CAML_LINENUM, 'number_style'),
 (
  stc.STC_CAML_NUMBER, 'number_style'),
 (
  stc.STC_CAML_OPERATOR, 'operator_style'),
 (
  stc.STC_CAML_STRING, 'string_style'),
 (
  stc.STC_CAML_TAGNAME, 'directive_style')]
if wx.VERSION >= (2, 9, 0, 0, ''):
    SYNTAX_ITEMS.append((stc.STC_CAML_WHITE, 'default_style'))
FOLD = ('fold', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Caml"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CAML)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         CAML_KW1, CAML_KW2, CAML_KW3]

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
         '(*', '*)']