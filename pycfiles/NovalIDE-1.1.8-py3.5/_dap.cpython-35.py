# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/syntax/lexer/_dap.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 1497 bytes
from noval import _
from noval.syntax import syndata, lang
import os, _python, noval.python.pyeditor as pyeditor, noval.imageutils as imageutils

class SyntaxLexer(_python.SyntaxLexer):
    __doc__ = 'SyntaxData object for Python'
    SYNTAX_ITEMS = []

    def __init__(self):
        lang_id = lang.RegisterNewLangId('ID_LANG_DAP')
        syndata.BaseLexer.__init__(self, lang_id)

    def GetDescription(self):
        return _('Cloudwms Dap File')

    def GetExt(self):
        return 'dap'

    def GetShowName(self):
        return 'Dap'

    def GetDefaultExt(self):
        return 'dap'

    def GetDocTypeName(self):
        return 'Dap Document'

    def GetViewTypeName(self):
        return _('Dap Editor')

    def GetDocTypeClass(self):
        return pyeditor.PythonDocument

    def GetViewTypeClass(self):
        return pyeditor.PythonView

    def GetDocIcon(self):
        return
        return imageutils.getPythonIcon()