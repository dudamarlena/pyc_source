# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_haxe.py
# Compiled at: 2011-08-30 21:43:46
"""
@summary: Lexer configuration module for haXe web programming language

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _haxe.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata, _cpp
HAXE_KW = (0, 'abstract break case catch class const continue trace do else enum extends finally for function goto if implements import in instanceof int interface new package private public return static super switch this throw throws transient try typeof var void volatile while with')
HAXE_TYPES = (1, 'Bool Enum false Float Int null String true Void ')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for HaXe"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, _cpp.AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         HAXE_KW, HAXE_TYPES, _cpp.DOC_KEYWORDS]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return _cpp.SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         _cpp.FOLD]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '//']