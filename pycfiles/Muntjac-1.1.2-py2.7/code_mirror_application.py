# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/codemirror/code_mirror_application.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.ui.check_box import CheckBox
from muntjac.api import Application, Window, GridLayout, Select, Button
from muntjac.data.property import IValueChangeListener
from muntjac.ui.button import IClickListener
from muntjac.addon.codemirror.client.code_mode import CodeMode
from muntjac.addon.codemirror.client.code_theme import CodeTheme
from muntjac.addon.codemirror.code_mirror import CodeMirror

class CodeMirrorApplication(Application):
    _NL = '\n\n'
    _SAMPLE_CODE = '<xml is="fun"></xml>' + _NL + 'function js(isMoreFun) {alert("Yay!");}' + _NL + 'public void java(String isAlsoCool) {\n\twith("Vaadin!");\n}' + _NL + 'def python(isCooler): print "with Muntjac!"' + _NL + 'select * from web where you = i;'

    def init(self):
        mainWindow = Window('CodeMirror Sample Application')
        hl = GridLayout(2, 5)
        hl.setSpacing(True)
        mainWindow.addComponent(hl)
        code = CodeMirror('Your Code', CodeMode.TEXT)
        code.setValue(self._SAMPLE_CODE)
        code.setWidth('500px')
        code.setHeight('350px')
        hl.addComponent(code)
        code2 = CodeMirror('Your Code Too', CodeMode.PYTHON)
        code2.setValue(self._SAMPLE_CODE)
        hl.addComponent(code2)
        codeMode = Select('Select your mode')
        for cs in CodeMode.values():
            codeMode.addItem(cs)

        codeMode.setNewItemsAllowed(False)
        codeMode.setNullSelectionAllowed(False)
        codeMode.setImmediate(True)
        hl.addComponent(codeMode)
        l = CodeModeChangeListener(code, codeMode)
        codeMode.addListener(l, IValueChangeListener)
        codeMode.setValue(CodeMode.TEXT)
        codeMode = Select('Select your mode too')
        for cs in CodeMode.values():
            codeMode.addItem(cs)

        codeMode.setNewItemsAllowed(False)
        codeMode.setNullSelectionAllowed(False)
        codeMode.setImmediate(True)
        hl.addComponent(codeMode)
        l = CodeModeChangeListener(code2, codeMode)
        codeMode.addListener(l, IValueChangeListener)
        codeMode.setValue(CodeMode.PYTHON)
        codeTheme = Select('Select your theme')
        for ct in CodeTheme.values():
            codeTheme.addItem(ct)

        codeTheme.setNewItemsAllowed(False)
        codeTheme.setImmediate(True)
        hl.addComponent(codeTheme)
        l = CodeThemeChangeListener(code, codeTheme)
        codeTheme.addListener(l, IValueChangeListener)
        codeTheme.setValue(CodeTheme.DEFAULT)
        codeTheme = Select('Select your theme too')
        for ct in CodeTheme.values():
            codeTheme.addItem(ct)

        codeTheme.setNewItemsAllowed(False)
        codeTheme.setImmediate(True)
        hl.addComponent(codeTheme)
        l = CodeThemeChangeListener(code2, codeTheme)
        codeTheme.addListener(l, IValueChangeListener)
        codeTheme.setValue(CodeTheme.ECLIPSE)
        l = CopyClickListener(code, code2)
        hl.addComponent(Button('copy to -->', l))
        l = CopyClickListener(code2, code)
        hl.addComponent(Button('<- copy to', l))
        l = ShowLineNumbersListener(code)
        cb = CheckBox('Show line numbers', l)
        cb.setImmediate(True)
        hl.addComponent(cb)
        l = ShowLineNumbersListener(code2)
        cb = CheckBox('Show line numbers', l)
        cb.setImmediate(True)
        hl.addComponent(cb)
        self.setMainWindow(mainWindow)


class CodeModeChangeListener(IValueChangeListener):

    def __init__(self, code, codeMode):
        self._code = code
        self._codeMode = codeMode

    def valueChange(self, event):
        self._code.setCodeMode(self._codeMode.getValue())


class CopyClickListener(IClickListener):

    def __init__(self, code1, code2):
        self._code1 = code1
        self._code2 = code2

    def buttonClick(self, event):
        self._code2.setValue(self._code1.getValue())


class CodeThemeChangeListener(IValueChangeListener):

    def __init__(self, code, codeTheme):
        self._code = code
        self._codeTheme = codeTheme

    def valueChange(self, event):
        self._code.setCodeTheme(self._codeTheme.getValue())


class ShowLineNumbersListener(IClickListener):

    def __init__(self, code):
        self._code = code

    def buttonClick(self, event):
        self._code.setShowLineNumbers(event.getButton().booleanValue())


if __name__ == '__main__':
    from muntjac.main import muntjac
    muntjac(CodeMirrorApplication, nogui=True, forever=True, debug=True)