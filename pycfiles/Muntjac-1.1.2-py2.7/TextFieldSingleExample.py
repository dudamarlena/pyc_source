# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/TextFieldSingleExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, TextField
from muntjac.data.property import IValueChangeListener

class TextFieldSingleExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(TextFieldSingleExample, self).__init__()
        self.setSpacing(True)
        self._editor = TextField('Echo this:')
        self._editor.addListener(self, IValueChangeListener)
        self._editor.setImmediate(True)
        self.addComponent(self._editor)

    def valueChange(self, event):
        self.getWindow().showNotification(self._editor.getValue())