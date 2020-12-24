# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_pascal.py
# Compiled at: 2010-12-05 17:39:29
"""
FILE: pascal.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Pacal.
@todo: Add Support for Turbo Pascal

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _pascal.py 66108 2010-11-10 21:04:54Z CJP $'
__revision__ = '$Revision: 66108 $'
import wx, wx.stc as stc, syndata
PAS_KEYWORDS = (0, 'and array asm begin case cdecl class const constructor default destructor div do downto else end end. except exit exports external far file finalization finally for function goto if implementation in index inherited initialization inline interface label library message mod near nil not object of on or out overload override packed pascal private procedure program property protected public published raise read record register repeat resourcestring safecall set shl shr stdcall stored string then threadvar to try type unit until uses var virtual while with write xor')
PAS_CLASSWORDS = (1, 'array boolean char integer file pointer real set string text variant write read default public protected private property published stored')
PAS_FUNCT = 'pack unpack Dispose New Abs Arctan Cos Exp Ln Sin Sqr Sqrt Eof Eoln Write Writeln Input Output Get Page Put Odd Pred Succ Chr Ord Round Trunc'
if wx.VERSION >= (2, 9, 0, 0, ''):
    SYNTAX_ITEMS = [
     (
      stc.STC_PAS_ASM, 'default_style'),
     (
      stc.STC_PAS_CHARACTER, 'char_style'),
     (
      stc.STC_PAS_COMMENT, 'comment_style'),
     (
      stc.STC_PAS_COMMENT2, 'comment_style'),
     (
      stc.STC_PAS_COMMENTLINE, 'comment_style'),
     (
      stc.STC_PAS_DEFAULT, 'default_style'),
     (
      stc.STC_PAS_HEXNUMBER, 'number_style'),
     (
      stc.STC_PAS_IDENTIFIER, 'default_style'),
     (
      stc.STC_PAS_NUMBER, 'number_style'),
     (
      stc.STC_PAS_OPERATOR, 'operator_style'),
     (
      stc.STC_PAS_PREPROCESSOR, 'pre_style'),
     (
      stc.STC_PAS_PREPROCESSOR2, 'default_style'),
     (
      stc.STC_PAS_STRING, 'string_style'),
     (
      stc.STC_PAS_STRINGEOL, 'stringeol_style'),
     (
      stc.STC_PAS_WORD, 'keyword_style')]
else:
    SYNTAX_ITEMS = [
     (
      stc.STC_C_DEFAULT, 'default_style'),
     (
      stc.STC_C_COMMENT, 'comment_style'),
     (
      stc.STC_C_COMMENTDOC, 'comment_style'),
     (
      stc.STC_C_COMMENTDOCKEYWORD, 'dockey_style'),
     (
      stc.STC_C_COMMENTDOCKEYWORDERROR, 'error_style'),
     (
      stc.STC_C_COMMENTLINE, 'comment_style'),
     (
      stc.STC_C_COMMENTLINEDOC, 'comment_style'),
     (
      stc.STC_C_CHARACTER, 'char_style'),
     (
      stc.STC_C_GLOBALCLASS, 'global_style'),
     (
      stc.STC_C_IDENTIFIER, 'default_style'),
     (
      stc.STC_C_NUMBER, 'number_style'),
     (
      stc.STC_C_OPERATOR, 'operator_style'),
     (
      stc.STC_C_PREPROCESSOR, 'pre_style'),
     (
      stc.STC_C_REGEX, 'pre_style'),
     (
      stc.STC_C_STRING, 'string_style'),
     (
      stc.STC_C_STRINGEOL, 'stringeol_style'),
     (
      stc.STC_C_UUID, 'pre_style'),
     (
      stc.STC_C_VERBATIM, 'number2_style'),
     (
      stc.STC_C_WORD, 'keyword_style'),
     (
      stc.STC_C_WORD2, 'keyword2_style')]
FOLD = ('fold', '1')
FLD_COMMENT = ('fold.comment', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Pascal"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_PASCAL)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         PAS_KEYWORDS, PAS_CLASSWORDS]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD, FLD_COMMENT]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '{', '}']