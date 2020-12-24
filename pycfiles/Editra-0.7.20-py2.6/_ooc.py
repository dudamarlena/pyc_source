# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_ooc.py
# Compiled at: 2011-08-30 21:43:47
"""
FILE: ooc.py                                                                
@author: Cody Precord                                                       
@summary: Lexer configuration file for OOC (Out of Class)
                                                                         
"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id:  $'
__revision__ = '$Revision:  $'
import wx.stc as stc, synglob, syndata, _cpp
KEYWORDS = (0, 'class cover interface implement func abstract extends from this super new const final static include import use extern inline proto break continue fallthrough operator if else for while do switch case as in version return true false null default')
TYPES = (1, 'Int Int8 Int16 Int32 Int64 Int80 Int128 UInt UInt8 UInt16 UInt32 UInt64 UInt80 UInt128 Octet Short UShort Long ULong LLong ULLong Float Double LDouble Float32 Float64 Float128 Char UChar WChar String Void Pointer Bool SizeT This')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for many OOC"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)

    def GetKeywords(self):
        """Returns Specified Keywords List"""
        return [
         KEYWORDS, TYPES, _cpp.DOC_KEYWORDS]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return _cpp.SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set"""
        return [
         _cpp.FOLD, _cpp.FOLD_COM]

    def GetCommentPattern(self):
        """Return comment pattern for OOC"""
        return [
         '//']