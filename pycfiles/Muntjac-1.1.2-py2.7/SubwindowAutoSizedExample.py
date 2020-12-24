# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/SubwindowAutoSizedExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Window, TextField, Button, Alignment
from muntjac.ui.button import IClickListener

class SubwindowAutoSizedExample(VerticalLayout):

    def __init__(self):
        super(SubwindowAutoSizedExample, self).__init__()
        self._subwindow = Window('Automatically sized subwindow')
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        layout.setSizeUndefined()
        for _ in range(7):
            tf = TextField()
            tf.setWidth('400px')
            self._subwindow.addComponent(tf)

        close = Button('Close', CloseListener(self))
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.BOTTOM_RIGHT)
        opn = Button('Open sized window', OpenListener(self))
        self.addComponent(opn)


class CloseListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._subwindow.getParent().removeWindow(self._c._subwindow)


class OpenListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is not None:
            self._c.getWindow().showNotification('Window is already open')
        else:
            self._c.getWindow().addWindow(self._c._subwindow)
        return