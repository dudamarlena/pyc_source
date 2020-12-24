# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_java.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: java.py
AUTHOR: Cody Precord
@summary: Lexer configuration file for Java source files.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _java.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
from _cpp import AutoIndenter
JAVA_KEYWORDS = (0, 'goto if else switch while for do this super new instanceof return throw try catch finally assert synchronize break continue ')
JAVA_KEYWORDS2 = (1, 'import native package synchronized throws extends implements interface class static synchronized transient volatile final serializable public protected private abstract')
JAVA_TYPES = (3, 'boolean char byte short int long float double void true false null String Integer Long Float Double Byte Boolean Map HashMap TreeMap CharSequence StringBuilder List ArrayList Set HashSet TreeSet Collection Exception System Runtime Collections Math ')
DOC_KEYWORDS = (2, 'TODO FIXME XXX \\author \\brief \\bug \\callgraph \\category \\class \\code \\date \\def \\depreciated \\dir \\dot \\dotfile \\else \\elseif \\em \\endcode \\enddot \\endif \\endverbatim \\example \\exception \\file \\if \\ifnot \\image \\include \\link \\mainpage \\name \\namespace \\page \\par \\paragraph \\param \\return \\retval \\section \\struct \\subpage \\subsection \\subsubsection \\test \\todo \\typedef \\union \\var \\verbatim \\version \\warning \\$ \\@ \\~ \\< \\> \\# \\% @param @return @throws HACK')
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
FOLD_PRE = ('styling.within.preprocessor', '0')
FOLD_COM = ('fold.comment', '1')
FOLD_COMP = ('fold.compact', '1')
FOLD_ELSE = ('fold.at.else', '0')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Java"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         JAVA_KEYWORDS, JAVA_KEYWORDS2, DOC_KEYWORDS, JAVA_TYPES]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD, FOLD_PRE]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '//']