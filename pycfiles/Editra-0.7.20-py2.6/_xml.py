# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_xml.py
# Compiled at: 2011-08-30 21:43:45
"""
FILE: xml.py
AUTHOR: Cody Precord
@summary: Lexer configuration module for XML Files.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _xml.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata, _html
XML_KEYWORDS = 'rss atom pubDate channel version title link description language generator item'

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for XML"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_XML)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, _html.AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        sgml = _html.KeywordString(synglob.ID_LANG_SGML)
        return [(5, XML_KEYWORDS + ' ' + sgml)]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return _html.SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         _html.FOLD, _html.FLD_HTML]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '<!--', '-->']