# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/SubwindowModalExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Window, Label, Button, Alignment
from muntjac.ui.button import IClickListener

class SubwindowModalExample(VerticalLayout):

    def __init__(self):
        super(SubwindowModalExample, self).__init__()
        self._subwindow = Window('A modal subwindow')
        self._subwindow.setModal(True)
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        message = Label('This is a modal subwindow.')
        self._subwindow.addComponent(message)
        close = Button('Close', CloseListener(self))
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.TOP_RIGHT)
        opn = Button('Open modal window', OpenListener(self))
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