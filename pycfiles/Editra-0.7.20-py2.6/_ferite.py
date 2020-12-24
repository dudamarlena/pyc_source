# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_ferite.py
# Compiled at: 2011-08-30 21:43:46
"""
@summary: Lexer configuration module for Ferite Scripting Language

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _ferite.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata, _cpp
FERITE_KW = (0, 'false null self super true abstract alias and arguments attribute_missing break case class closure conformsToProtocol constructor continue default deliver destructor diliver directive do else extends eval final fix for function global handle if iferr implements include instanceof isa method_missing modifies monitor namespace new or private protected protocol public raise recipient rename return static switch uses using while')
FERITE_TYPES = (1, 'boolean string number array object void XML Unix Sys String Stream Serialize RMI Posix Number Network Math FileSystem Console Array Regexp XSLT')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for Ferite"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_CPP)
        self.RegisterFeature(synglob.FEATURE_AUTOINDENT, _cpp.AutoIndenter)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         FERITE_KW, FERITE_TYPES, _cpp.DOC_KEYWORDS]

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