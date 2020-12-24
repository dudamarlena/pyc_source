# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_smalltalk.py
# Compiled at: 2011-08-30 21:43:47
"""
FILE: smalltalk.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Smalltalk
@todo: more keywords, styling fixes

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _smalltalk.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
ST_KEYWORDS = (0, 'ifTrue: ifFalse: whileTrue: whileFalse: ifNil: ifNotNil: whileTrue repeat isNil put to at notNil super self true false new not isNil inspect out nil do add for methods methodsFor instanceVariableNames classVariableNames poolDictionaries subclass')
SYNTAX_ITEMS = [
 (
  stc.STC_ST_ASSIGN, 'operator_style'),
 (
  stc.STC_ST_BINARY, 'operator_style'),
 (
  stc.STC_ST_BOOL, 'keyword_style'),
 (
  stc.STC_ST_CHARACTER, 'char_style'),
 (
  stc.STC_ST_COMMENT, 'comment_style'),
 (
  stc.STC_ST_DEFAULT, 'default_style'),
 (
  stc.STC_ST_GLOBAL, 'global_style'),
 (
  stc.STC_ST_KWSEND, 'keyword_style'),
 (
  stc.STC_ST_NIL, 'keyword_style'),
 (
  stc.STC_ST_NUMBER, 'number_style'),
 (
  stc.STC_ST_RETURN, 'keyword_style'),
 (
  stc.STC_ST_SELF, 'keyword_style'),
 (
  stc.STC_ST_SPECIAL, 'pre_style'),
 (
  stc.STC_ST_SPEC_SEL, 'keyword_style'),
 (
  stc.STC_ST_STRING, 'string_style'),
 (
  stc.STC_ST_SUPER, 'class_style'),
 (
  stc.STC_ST_SYMBOL, 'scalar_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Smalltalk"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_SMALLTALK)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         ST_KEYWORDS]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '"', '"']


def KeywordString():
    """Returns the specified Keyword String
    @note: not used by most modules

    """
    return ST_KEYWORDS[1]