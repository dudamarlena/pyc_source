# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/lexer/_h.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1910 bytes
from noval import _
from noval.syntax import syndata, lang
import noval.util.appdirs as appdirs, os, noval.editor.code as codeeditor, noval.imageutils as imageutils, re, _cpp, _c

class SyntaxLexer(_c.SyntaxLexer):
    __doc__ = 'SyntaxData object for Python'
    SYNTAX_ITEMS = []

    def __init__(self):
        lang_id = lang.RegisterNewLangId('ID_LANG_H')
        syndata.BaseLexer.__init__(self, lang_id)

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetDescription(self):
        return _('C/C++ Header File')

    def GetExt(self):
        return 'h'

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '/*', '*/']

    def GetShowName(self):
        return 'C/C++'

    def GetDefaultExt(self):
        return 'h'

    def GetDocTypeName(self):
        return 'C/C++ Header Document'

    def GetViewTypeName(self):
        return _('C/C++ Header Editor')

    def GetDocTypeClass(self):
        return codeeditor.CodeDocument

    def GetViewTypeClass(self):
        return codeeditor.CodeView

    def GetDocIcon(self):
        return imageutils.load_image('', 'file/h_file.gif')

    def GetColorClass(self):
        return _cpp.SyntaxColorer

    def IsVisible(self):
        return False