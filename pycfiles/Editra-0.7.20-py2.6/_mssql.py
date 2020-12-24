# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_mssql.py
# Compiled at: 2011-08-30 21:43:45
"""
FILE: mssql.py                                                              
AUTHOR: Cody Precord                                                        
@summary: Lexer configuration module for Microsoft SQL.
@todo: too many to list                                                     

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _mssql.py 68355 2011-07-24 20:06:07Z CJP $'
__revision__ = '$Revision: 68355 $'
import wx.stc as stc, syndata
MSSQL_DAT = (0, '')
MSSQL_SYS = (1, '')
MSSQL_GLOB = (2, '')
MSSQL_FUNC = (3, '')
MSSQL_SYSP = (4, '')
MSSQL_OPS = (5, '')
SYNTAX_ITEMS = [
 (
  stc.STC_MSSQL_DEFAULT, 'default_style'),
 (
  stc.STC_MSSQL_COMMENT, 'comment_style'),
 (
  stc.STC_MSSQL_COLUMN_NAME, 'keyword_style'),
 (
  stc.STC_MSSQL_COLUMN_NAME_2, 'keyword_style'),
 (
  stc.STC_MSSQL_DATATYPE, 'keyword2_style'),
 (
  stc.STC_MSSQL_DEFAULT_PREF_DATATYPE, 'class_style'),
 (
  stc.STC_MSSQL_FUNCTION, 'keyword3_style'),
 (
  stc.STC_MSSQL_GLOBAL_VARIABLE, 'global_style'),
 (
  stc.STC_MSSQL_IDENTIFIER, 'default_style'),
 (
  stc.STC_MSSQL_LINE_COMMENT, 'comment_style'),
 (
  stc.STC_MSSQL_NUMBER, 'number_style'),
 (
  stc.STC_MSSQL_OPERATOR, 'operator_style'),
 (
  stc.STC_MSSQL_STATEMENT, 'keyword_style'),
 (
  stc.STC_MSSQL_STORED_PROCEDURE, 'scalar2_style'),
 (
  stc.STC_MSSQL_STRING, 'string_style'),
 (
  stc.STC_MSSQL_SYSTABLE, 'keyword4_style'),
 (
  stc.STC_MSSQL_VARIABLE, 'scalar_style')]
FOLD = ('fold', '1')
FOLD_COMMENT = ('fold.comment', '1')
FOLD_COMPACT = ('fold.compact', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for MS SQL"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_MSSQL)

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
         '--']