# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_vbscript.py
# Compiled at: 2011-08-30 21:43:45
"""
FILE: vbscript.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for VBScript.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _vbscript.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
VBS_KW = 'addressof alias and as attribute base begin binary boolean byref byte byval call case cdbl cint clng compare const csng cstr currency date decimal declare defbool defbyte defcur defdate defdbl defdec defint deflng defobj defsng defstr defvar dim do double each else elseif empty end enum eqv erase error event exit explicit false for friend function get global gosub goto if imp implements in input integer is len let lib like load lock long loop lset me mid midb mod new next not nothing null object on option optional or paramarray preserve print private property public raiseevent randomize redim rem resume return rset seek select set single static step stop string sub text then time to true type typeof unload until variant wend while with withevents xor'
SYNTAX_ITEMS = [
 (
  stc.STC_B_ASM, 'asm_style'),
 (
  stc.STC_B_BINNUMBER, 'default_style'),
 (
  stc.STC_B_COMMENT, 'comment_style'),
 (
  stc.STC_B_CONSTANT, 'const_style'),
 (
  stc.STC_B_DATE, 'default_style'),
 (
  stc.STC_B_DEFAULT, 'default_style'),
 (
  stc.STC_B_ERROR, 'error_style'),
 (
  stc.STC_B_HEXNUMBER, 'number_style'),
 (
  stc.STC_B_IDENTIFIER, 'default_style'),
 (
  stc.STC_B_KEYWORD, 'keyword_style'),
 (
  stc.STC_B_KEYWORD2, 'class_style'),
 (
  stc.STC_B_KEYWORD3, 'funct_style'),
 (
  stc.STC_B_KEYWORD4, 'scalar_style'),
 (
  stc.STC_B_LABEL, 'directive_style'),
 (
  stc.STC_B_NUMBER, 'number_style'),
 (
  stc.STC_B_OPERATOR, 'operator_style'),
 (
  stc.STC_B_PREPROCESSOR, 'pre_style'),
 (
  stc.STC_B_STRING, 'string_style'),
 (
  stc.STC_B_STRINGEOL, 'stringeol_style')]
FOLD = ('fold', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for VbScript"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_VBSCRIPT)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         (
          0, VBS_KW)]

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
         "'"]