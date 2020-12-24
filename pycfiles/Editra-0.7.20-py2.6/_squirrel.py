# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_squirrel.py
# Compiled at: 2011-08-30 21:43:45
"""
@summary: Lexer configuration module for Squirrel Programming Language

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _squirrel.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata, _cpp
SQUIRREL_KW = (0, 'break case catch class clone continue const default delegate delete do else enum extends for foreach function if in local null resume return switch this throw try typeof while parent yield constructor vargc vargv instanceof true false static')
SQUIRREL_TYPES = (1, '')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Squirrel"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, _cpp.AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         SQUIRREL_KW, SQUIRREL_TYPES, _cpp.DOC_KEYWORDS]

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