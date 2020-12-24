# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_matlab.py
# Compiled at: 2011-08-30 21:43:47
"""
FILE: matlab.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Matlab and Octave

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _matlab.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
MATLAB_KW = (0, 'break case catch continue else elseif end for function global if otherwise persistent return switch try while')
OCTAVE_KW = (0, 'break case catch continue do else elseif end end_unwind_protect endfor endif endswitch endwhile for function endfunction global if otherwise persistent return switch try until unwind_protect unwind_protect_cleanup while')
SYNTAX_ITEMS = [
 (
  stc.STC_MATLAB_COMMAND, 'funct_style'),
 (
  stc.STC_MATLAB_COMMENT, 'comment_style'),
 (
  stc.STC_MATLAB_DEFAULT, 'default_style'),
 (
  stc.STC_MATLAB_DOUBLEQUOTESTRING, 'string_style'),
 (
  stc.STC_MATLAB_IDENTIFIER, 'default_style'),
 (
  stc.STC_MATLAB_KEYWORD, 'keyword_style'),
 (
  stc.STC_MATLAB_NUMBER, 'number_style'),
 (
  stc.STC_MATLAB_OPERATOR, 'operator_style'),
 (
  stc.STC_MATLAB_STRING, 'string_style')]
FOLD = ('fold', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for MatLab and Octave"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        if self.LangId == synglob.ID_LANG_MATLAB:
            self.SetLexer(stc.STC_LEX_MATLAB)
        else:
            self.SetLexer(stc.STC_LEX_OCTAVE)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        if self.LangId == synglob.ID_LANG_MATLAB:
            return [MATLAB_KW]
        else:
            if self.LangId == synglob.ID_LANG_OCTAVE:
                return [OCTAVE_KW]
            return list()

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        if self.LangId == synglob.ID_LANG_MATLAB:
            return ['%']
        else:
            if self.LangId == synglob.ID_LANG_OCTAVE:
                return ['#']
            return list()