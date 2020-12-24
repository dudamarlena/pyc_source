# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_asm.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: asm.py
AUTHOR: Cody Precord
@summary: Lexer configuration file GNU Assembly Code
@todo: Complete Keywords/Registers

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _asm.py 70228 2011-12-31 20:39:16Z CJP $'
__revision__ = '$Revision: 70228 $'
import wx.stc as stc, synglob, syndata
ASM_CPU_INST = (0, '.long .ascii .asciz .byte .double .float .hword .int .octa .quad .short .single .space .string .word')
ASM_MATH_INST = (1, '')
ASM_REGISTER = (2, '')
ASM_DIRECTIVES = (3, '.include .macro .endm')
SYNTAX_ITEMS = [
 (
  stc.STC_ASM_DEFAULT, 'default_style'),
 (
  stc.STC_ASM_CHARACTER, 'char_style'),
 (
  stc.STC_ASM_COMMENT, 'comment_style'),
 (
  stc.STC_ASM_COMMENTBLOCK, 'comment_style'),
 (
  stc.STC_ASM_CPUINSTRUCTION, 'keyword_style'),
 (
  stc.STC_ASM_DIRECTIVE, 'keyword3_style'),
 (
  stc.STC_ASM_DIRECTIVEOPERAND, 'default_style'),
 (
  stc.STC_ASM_EXTINSTRUCTION, 'default_style'),
 (
  stc.STC_ASM_IDENTIFIER, 'default_style'),
 (
  stc.STC_ASM_MATHINSTRUCTION, 'keyword_style'),
 (
  stc.STC_ASM_NUMBER, 'number_style'),
 (
  stc.STC_ASM_OPERATOR, 'operator_style'),
 (
  stc.STC_ASM_REGISTER, 'keyword2_style'),
 (
  stc.STC_ASM_STRING, 'string_style'),
 (
  stc.STC_ASM_STRINGEOL, 'stringeol_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Assembly files"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_ASM)

    def GetKeywords(self):
        """Returns List of Keyword Specifications """
        return [
         ASM_CPU_INST, ASM_DIRECTIVES]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         ';']