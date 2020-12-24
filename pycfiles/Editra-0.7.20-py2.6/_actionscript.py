# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_actionscript.py
# Compiled at: 2012-03-17 12:57:53
"""
FILE: actionscript.py                                                                
AUTHOR: Cody Precord                                                       
@summary: Lexer configuration file for ActionScript
                                                                         
"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _actionscript.py 70228 2011-12-31 20:39:16Z CJP $'
__revision__ = '$Revision: 70228 $'
import wx.stc as stc, synglob, syndata, _cpp
AS_KEYWORDS = 'break case catch continue default do each else finally for if in label new return super switch throw while with dynamic final internal native override private protected public static class const extends function get implements interface namespace package set var import include use false null this true void Null *'
AS_TYPES = 'AS3 flash_proxy object_proxy flash accessibility display errors events external filters geom media net printing profiler system text ui utils xml '

class SyntaxData(syndata.SyntaxDataBase):
    """ActionScript SyntaxData"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, _cpp.AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         (
          0, AS_KEYWORDS), (1, AS_TYPES)]

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return _cpp.SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         _cpp.FOLD, _cpp.FOLD_PRE]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '//']