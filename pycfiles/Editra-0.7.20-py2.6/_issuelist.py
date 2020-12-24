# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_issuelist.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: issuelist.py
AUTHOR: Cody Precord, Torsten Mohr
@summary: Lexer configuration module for Issue Lists.

"""
__author__ = 'Cody Precord <cprecord>, Torsten Mohr <none_yet>'
__svnid__ = '$Id: _issuelist.py 70229 2012-01-01 01:27:10Z CJP $'
__revision__ = '$Revision: 70229 $'
import wx.stc as stc, synglob, syndata
(STC_ISSL_DEFAULT, STC_ISSL_COMMENT, STC_ISSL_GREEN, STC_ISSL_RED, STC_ISSL_ORANGE, STC_ISSL_BLUE, STC_ISSL_PURPLE, STC_ISSL_PINK) = range(8)
SYNTAX_ITEMS = [
 (
  STC_ISSL_DEFAULT, 'default_style'),
 (
  STC_ISSL_COMMENT, 'comment_style'),
 (
  STC_ISSL_GREEN, 'regex_style'),
 (
  STC_ISSL_RED, 'number_style'),
 (
  STC_ISSL_ORANGE, 'keyword4_style'),
 (
  STC_ISSL_BLUE, 'dockey_style'),
 (
  STC_ISSL_PURPLE, 'scalar2_style'),
 (
  STC_ISSL_PINK, 'char_style')]
issl_table = ';+-?.#~'

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for IssueLists
    This class is primarly intended as an example to creating a custom
    lexer

    """

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CONTAINER)
        self.RegisterFeature(synglob.FEATURE_STYLETEXT, StyleText)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS


def StyleText(stc, start, end):
    """Style the text
    @param stc: Styled text control instance
    @param start: Start position
    @param end: end position

    """
    line = stc.LineFromPosition(start)
    while line > 0 and stc.GetLineState(line) == 0:
        line -= 1

    eline = stc.LineFromPosition(end)
    state = stc.GetLineState(line) - 1
    if state < 0:
        state = 0
    for ln in range(line, eline + 1):
        text = stc.GetLine(ln).encode('utf-8')
        len_text = len(text)
        text = text.strip()
        if len(text) == 0:
            state = 0
        elif len(text) > 0:
            ch = text[0]
            ix = issl_table.find(ch)
            if ix >= 0:
                state = ix + 1
        stc.StartStyling(stc.PositionFromLine(ln), 255)
        stc.SetStyling(len_text, state)
        stc.SetLineState(ln, state + 1)