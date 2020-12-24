# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_groovy.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: groovy.py
AUTHOR: Omar Gomez
@summary: Lexer configuration module for Groovy (based on the Java one).

"""
__author__ = 'Omar Gomez <omar.gomez@gmail.com>'
__svnid__ = '$Id: _groovy.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
from _cpp import AutoIndenter
MAIN_KEYWORDS = (0, '\nas assert Boolean Byte Character Class Double Float Integer Long Number Object \nShort String property void abstract assert boolean break byte case catch char \nclass const continue default do double else extends false final finally float \nfor goto if implements import instanceof in int interface long native new null \npackage private protected public return short static strictfp super switch \nsynchronized this throw throws transient true try void volatile while def\n')
SECONDARY_KEYWORDS = (1, '\nabs accept allProperties and any append asImmutable asSynchronized asWritable \ncenter collect compareTo contains count decodeBase64 div dump each eachByte \neachFile eachFileRecurse eachLine eachMatch eachProperty eachPropertyName \neachWithIndex encodeBase64 every execute filterLine find findAll findIndexOf \nflatten getErr getIn getOut getText inject inspect intersect intdiv invokeMethod \nisCase join leftShift max min minus mod multiply negate newInputStream \nnewOutputStream newPrintWriter newReader newWriter next or padLeft padRight \nplus pop previous print println readBytes readLine readLines reverse \nreverseEach rightShift rightShiftUnsigned round size sort splitEachLine step \nsubMap times toDouble toFloat toInteger tokenize toList toLong toURL \ntransformChar transformLine upto use waitForOrKill withInputStream \nwithOutputStream withPrintWriter withReader withStream withStreams withWriter \nwithWriterAppend write writeLine\n')
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
    """SyntaxData object for Groovy"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         MAIN_KEYWORDS, SECONDARY_KEYWORDS]

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