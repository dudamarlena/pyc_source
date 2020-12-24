# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/SubwindowPositionedExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Window, Label, Button, Alignment
from muntjac.ui import button

class SubwindowPositionedExample(VerticalLayout):

    def __init__(self):
        super(SubwindowPositionedExample, self).__init__()
        self.setSpacing(True)
        self._subwindow = Window('A positioned subwindow')
        self._subwindow.setWidth('300px')
        self._subwindow.setHeight('200px')
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        layout.setSizeFull()
        message = Label('This is a positioned window')
        self._subwindow.addComponent(message)
        close = Button('Close', CloseListener(self))
        layout.addComponent(close)
        layout.setComponentAlignment(close, Alignment.BOTTOM_RIGHT)
        fifty = Button('Open window at position 50x50', OpenListener50(self))
        self.addComponent(fifty)
        onefifty = Button('Open window at position 150x200', OpenListener150(self))
        self.addComponent(onefifty)
        center = Button('Open centered window', CenterListener(self))
        self.addComponent(center)


class CloseListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c._subwindow.getParent().removeWindow(self._c._subwindow)


class OpenListener50(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is None:
            self._c.getWindow().addWindow(self._c._subwindow)
        self._c._subwindow.setPositionX(50)
        self._c._subwindow.setPositionY(50)
        return


class OpenListener150(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is None:
            self._c.getWindow().addWindow(self._c._subwindow)
        self._c._subwindow.setPositionX(150)
        self._c._subwindow.setPositionY(200)
        return


class CenterListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is None:
            self._c.getWindow().addWindow(self._c._subwindow)
        self._c._subwindow.center()
        return