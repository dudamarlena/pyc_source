# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_boo.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: boo.py
@summary: Defines language and syntax highlighting settings for the Boo
          programming language
@todo: support for C style comment regions
"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _boo.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata, _python
BOO_KW = (0, 'abstract and as AST break callable cast char class constructor continue def destructor do elif else ensure enum event except failure final false for from get given goto if import in interface internal is isa not null of or otherwise override namespace partial pass private protected public raise ref retry return self set static super struct success transient true try typeof unless virtual when while yield')
SYNTAX_ITEMS = [ x for x in _python.SYNTAX_ITEMS if x[0] != stc.STC_P_DECORATOR ]
SYNTAX_ITEMS.append((stc.STC_P_DECORATOR, 'default_style'))
FOLD = ('fold', '1')
TIMMY = ('tab.timmy.whinge.level', '1')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Boo
    @todo: needs custom highlighting handler

    """

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_PYTHON)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         BOO_KW]

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