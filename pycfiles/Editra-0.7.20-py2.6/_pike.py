# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_pike.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: pike.py
@summary: Defines syntax and highlighting settings for the Pike programming
          language. Pike is very similar in form to C/CPP so the Cpp lexer is
          used to provide the highlighting settings.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _pike.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata, _cpp
PIKE_KW = (0, 'goto break return continue case default if else switch while foreach do gauge destruct lambda inherit import typeof catch for inline nomask')
PIKE_TYPE = (1, 'private protected public static int string void float mapping array multiset mixed program object function')

class SyntaxData(_cpp.SyntaxData):
    """SyntaxData object for Pike"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        return [
         PIKE_KW, PIKE_TYPE, _cpp.DOC_KEYWORDS]

    def GetCommentPattern(self):
        """Get the comment pattern"""
        return [
         '//']