# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_forth.py
# Compiled at: 2011-08-30 21:43:47
"""
FILE: _forth.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for Forth

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _forth.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
CONTROL_KW = (0, 'again begin case do else endcase endof if loop of repeat then until while [if] [else] [then] ?do')
KEYWORDS = (1, 'dup drop rot swap over @ ! 2@ 2! 2dup 2drop 2swap 2over nip r@ >r r&gt; 2r@ 2>r 2r>; 0= 0<; sp@ sp! w@ w! c@ c! < > = <> 0<> space spaces key? key throw catch abort */ 2* /mod cell+ cells char+ chars move erase dabs title hex decimal hold <# # #s #> sign d. . u. dump (.") >number \' immediate exit recurse unloop leave here allot , c, w, compile, branch, ret, lit, dlit, ?branch, ", >mark >resolve1 <mark >resolve align aligned user-allot user-here header does> smudge hide :noname last-word ?error error2 find1 sfind set-current get-current definitions get-order forth only set-order also previous voc-name. order latest literal 2literal sliteral cliteral ?literal1 ?sliteral1 hex-literal hex-sliteral ?literal2 ?sliteral2 source EndOfChunk CharAddr PeekChar IsDelimiter GetChar OnDelimiter SkipDelimiters OnNotDelimiter SkipWord SkipUpTo ParseWord NextWord parse skip console-handles refill depth ?stack ?comp word interpret bye quit main1 evaluate include-file included >body +word wordlist class! class@ par! par@ id. ?immediate ?voc immediate VOC WordByAddrWl WordByAddr nlist words save options /notransl ansi>oem accept emit cr type ekey? ekey ekey>char externtask erase-imports ModuleName ModuleDirName environment? drop-exc-handler set-exc-handler halt err close-file create-file create-file-shared open-file-shared delete-file file-position file-size open-file read-file reposition-file dos-lines unix-lines read-line write-file resize-file write-line allocate free resize start suspend resume stop pause min max true false asciiz> r/o w/o ;class endwith or and /string search compare export ;module space')
DEFINITION_KW = (2, 'variable create : value constant vm: m: var dvar chars obj constr: destr: class: object: pointer user user-create user-value vect wndproc: vocabulary -- task: cez: module:')
PREWORDS1 = (3, "CHAR [CHAR] POSTPONE WITH ['] TO [COMPILE] CHAR ASCII \\'")
PREWORDS2 = (4, 'REQUIRE WINAPI:')
STRING_DEF_KW = (5, 'S" ABORT" Z" " ." C"')
SYNTAX_ITEMS = [
 (
  stc.STC_FORTH_DEFAULT, 'default_style'),
 (
  stc.STC_FORTH_COMMENT, 'comment_style'),
 (
  stc.STC_FORTH_COMMENT_ML, 'comment_style'),
 (
  stc.STC_FORTH_KEYWORD, 'keyword_style'),
 (
  stc.STC_FORTH_NUMBER, 'number_style'),
 (
  stc.STC_FORTH_PREWORD1, 'keyword2_style'),
 (
  stc.STC_FORTH_PREWORD2, 'keyword3_style'),
 (
  stc.STC_FORTH_STRING, 'string_style')]

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Forth"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_FORTH)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         CONTROL_KW, KEYWORDS, DEFINITION_KW,
         PREWORDS1, PREWORDS2, STRING_DEF_KW]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '\\ ']