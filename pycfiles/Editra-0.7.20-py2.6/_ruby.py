# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_ruby.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: ruby.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Ruby.
@todo: Default Style Refinement.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _ruby.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, re, synglob, syndata
RUBY_KW = (0, '__FILE__ and def end in or self unless __LINE__ begin defined ensure module redo super until BEGIN break do false next require rescue then when END case else for nil retry true while alias class elsif if not return undef yieldr puts raise protected private')
SYNTAX_ITEMS = [
 (
  stc.STC_RB_BACKTICKS, 'scalar_style'),
 (
  stc.STC_RB_CHARACTER, 'char_style'),
 (
  stc.STC_RB_CLASSNAME, 'class_style'),
 (
  stc.STC_RB_CLASS_VAR, 'default_style'),
 (
  stc.STC_RB_COMMENTLINE, 'comment_style'),
 (
  stc.STC_RB_DATASECTION, 'default_style'),
 (
  stc.STC_RB_DEFAULT, 'default_style'),
 (
  stc.STC_RB_DEFNAME, 'keyword3_style'),
 (
  stc.STC_RB_ERROR, 'error_style'),
 (
  stc.STC_RB_GLOBAL, 'global_style'),
 (
  stc.STC_RB_HERE_DELIM, 'default_style'),
 (
  stc.STC_RB_HERE_Q, 'here_style'),
 (
  stc.STC_RB_HERE_QQ, 'here_style'),
 (
  stc.STC_RB_HERE_QX, 'here_style'),
 (
  stc.STC_RB_IDENTIFIER, 'default_style'),
 (
  stc.STC_RB_INSTANCE_VAR, 'scalar2_style'),
 (
  stc.STC_RB_MODULE_NAME, 'global_style'),
 (
  stc.STC_RB_NUMBER, 'number_style'),
 (
  stc.STC_RB_OPERATOR, 'operator_style'),
 (
  stc.STC_RB_POD, 'default_style'),
 (
  stc.STC_RB_REGEX, 'regex_style'),
 (
  stc.STC_RB_STDIN, 'default_style'),
 (
  stc.STC_RB_STDOUT, 'default_style'),
 (
  stc.STC_RB_STRING, 'string_style'),
 (
  stc.STC_RB_STRING_Q, 'default_style'),
 (
  stc.STC_RB_STRING_QQ, 'default_style'),
 (
  stc.STC_RB_STRING_QR, 'default_style'),
 (
  stc.STC_RB_STRING_QW, 'default_style'),
 (
  stc.STC_RB_STRING_QX, 'default_style'),
 (
  stc.STC_RB_SYMBOL, 'default_style'),
 (
  stc.STC_RB_UPPER_BOUND, 'default_style'),
 (
  stc.STC_RB_WORD, 'keyword_style'),
 (
  stc.STC_RB_WORD_DEMOTED, 'keyword2_style')]
FOLD = ('fold', '1')
TIMMY = ('fold.timmy.whinge.level', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Ruby"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_RUBY)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         RUBY_KW]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD, TIMMY]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '#']


def AutoIndenter(estc, pos, ichar):
    """Auto indent cpp code.
    @param estc: EditraStyledTextCtrl
    @param pos: current carat position
    @param ichar: Indentation character

    """
    rtxt = ''
    line = estc.GetCurrentLine()
    text = estc.GetTextRange(estc.PositionFromLine(line), pos)
    eolch = estc.GetEOLChar()
    indent = estc.GetLineIndentation(line)
    if ichar == '\t':
        tabw = estc.GetTabWidth()
    else:
        tabw = estc.GetIndent()
    i_space = indent / tabw
    ndent = eolch + ichar * i_space
    rtxt = ndent + (indent - tabw * i_space) * ' '
    def_pat = re.compile('\\s*(class|def)\\s+[a-zA-Z_][a-zA-Z0-9_]*')
    text = text.strip()
    if text.endswith('{') or def_pat.match(text):
        rtxt += ichar
    estc.AddText(rtxt)


def KeywordString(option=0):
    """Returns the specified Keyword String
    @note: not used by most modules

    """
    return RUBY_KW[1]