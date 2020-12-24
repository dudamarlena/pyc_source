# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_erlang.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: erlang.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for the Erlang Programming Language
@todo: better styling

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _erlang.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx, wx.stc as stc, synglob, syndata
KEYWORDS = (0, 'compile define else endif export file ifdef ifndef import include include_lib module record undef author copyright doc after begin case catch cond end fun if let of query receive when define record export import include include_lib else endif undef apply attribute call do in letrec module primop try')
SYNTAX_ITEMS = [
 (
  stc.STC_ERLANG_ATOM, 'default_style'),
 (
  stc.STC_ERLANG_CHARACTER, 'char_style'),
 (
  stc.STC_ERLANG_COMMENT, 'comment_style'),
 (
  stc.STC_ERLANG_DEFAULT, 'default_style'),
 (
  stc.STC_ERLANG_FUNCTION_NAME, 'funct_style'),
 (
  stc.STC_ERLANG_KEYWORD, 'keyword_style'),
 (
  stc.STC_ERLANG_MACRO, 'pre_style'),
 (
  stc.STC_ERLANG_NODE_NAME, 'string_style'),
 (
  stc.STC_ERLANG_NUMBER, 'number_style'),
 (
  stc.STC_ERLANG_OPERATOR, 'operator_style'),
 (
  stc.STC_ERLANG_RECORD, 'keyword2_style'),
 (
  stc.STC_ERLANG_STRING, 'string_style'),
 (
  stc.STC_ERLANG_UNKNOWN, 'unknown_style'),
 (
  stc.STC_ERLANG_VARIABLE, 'default_style')]
if wx.VERSION >= (2, 9, 0, 0, ''):
    SYNTAX_ITEMS.append((stc.STC_ERLANG_ATOM_QUOTED, 'default_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_BIFS, 'default_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_COMMENT_DOC, 'dockey_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_COMMENT_DOC_MACRO, 'dockey_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_COMMENT_FUNCTION, 'comment_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_COMMENT_MODULE, 'comment_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_MACRO_QUOTED, 'default_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_MODULES, 'default_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_MODULES_ATT, 'default_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_NODE_NAME_QUOTED, 'default_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_PREPROC, 'pre_style'))
    SYNTAX_ITEMS.append((stc.STC_ERLANG_RECORD_QUOTED, 'default_style'))
else:
    SYNTAX_ITEMS.append((stc.STC_ERLANG_SEPARATOR, 'default_style'))
FOLD = ('fold', '1')
FOLD_CMT = ('fold.comments', '1')
FOLD_KW = ('fold.keywords', '1')
FOLD_BRACE = ('fold.braces', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Erlang"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_ERLANG)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         KEYWORDS]

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
         '%%']