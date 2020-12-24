# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/codemirror/code_mirror.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.ui.text_field import TextField
from muntjac.addon.codemirror.client.code_mode import CodeMode
from muntjac.addon.codemirror.client.code_theme import CodeTheme

class CodeMirror(TextField):
    """Server side component for the VCodeMirrorTextField2 widget."""
    CLIENT_WIDGET = None
    TYPE_MAPPING = 'org.vaadin.codemirror2.CodeMirror'

    def __init__(self, caption, codeMode=None, codeTheme=None):
        if codeMode is None:
            codeMode = CodeMode.TEXT
        if codeTheme is None:
            codeTheme = CodeTheme.DEFAULT
        self._codeStyle = None
        self._showLineNumbers = False
        self._codeTheme = None
        super(CodeMirror, self).__init__(caption)
        self.setCodeMode(codeMode)
        self.setCodeTheme(codeTheme)
        return

    def paintContent(self, target):
        super(CodeMirror, self).paintContent(target)
        if self.getCodeMode() is not None:
            target.addAttribute('codeMode', self.getCodeMode().getId())
        target.addAttribute('showLineNumbers', self.isShowLineNumbers())
        if self.getCodeTheme() is not None:
            target.addAttribute('codeTheme', self.getCodeTheme().getId())
        return

    def setCodeMode(self, codeMode):
        self._codeMode = codeMode
        self.requestRepaint()

    def getCodeMode(self):
        return self._codeMode

    def setShowLineNumbers(self, showLineNumbers):
        self._showLineNumbers = showLineNumbers
        self.requestRepaint()

    def isShowLineNumbers(self):
        return self._showLineNumbers

    def setCodeTheme(self, codeTheme):
        self._codeTheme = codeTheme
        self.requestRepaint()

    def getCodeTheme(self):
        return self._codeTheme