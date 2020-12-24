# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/TextAreaExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import HorizontalLayout, Button, Label, TextArea
from muntjac.data.property import IValueChangeListener

class TextAreaExample(HorizontalLayout, IValueChangeListener):
    _initialText = 'The quick brown fox jumps over the lazy dog.'

    def __init__(self):
        super(TextAreaExample, self).__init__()
        self.setSpacing(True)
        self.setWidth('100%')
        self._editor = TextArea(None, self._initialText)
        self._editor.setRows(20)
        self._editor.setColumns(20)
        self._editor.addListener(self, IValueChangeListener)
        self._editor.setImmediate(True)
        self.addComponent(self._editor)
        self.addComponent(Button('>'))
        self._plainText = Label(self._initialText)
        self._plainText.setContentMode(Label.CONTENT_XHTML)
        self.addComponent(self._plainText)
        self.setExpandRatio(self._plainText, 1)
        return

    def valueChange(self, event):
        text = self._editor.getValue()
        if text is not None:
            text = text.replace('\n', '<br/>')
        self._plainText.setValue(text)
        return