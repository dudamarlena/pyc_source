# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/SubwindowCloseExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, CheckBox, Window, Label, Button
from muntjac.data.property import IValueChangeListener
from muntjac.ui.window import ICloseListener
from muntjac.ui.button import IClickListener

class SubwindowCloseExample(VerticalLayout):
    _openWindowText = 'Open a window'
    _closeWindowText = 'Close the window'

    def __init__(self):
        super(SubwindowCloseExample, self).__init__()
        self._closableWindow = CheckBox('Allow user to close the window', True)
        self._closableWindow.setImmediate(True)
        self._closableWindow.addListener(ClosableChangeListener(self), IValueChangeListener)
        self._subwindow = Window('A subwindow w/ close-listener')
        self._subwindow.addListener(CloseListener(self), ICloseListener)
        layout = self._subwindow.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        message = Label('This is a subwindow with a close-listener.')
        self._subwindow.addComponent(message)
        self._openCloseButton = Button('Open window', ClickListener(self))
        self.setSpacing(True)
        self.addComponent(self._closableWindow)
        self.addComponent(self._openCloseButton)


class ClosableChangeListener(IValueChangeListener):

    def __init__(self, c):
        self._c = c

    def valueChange(self, event):
        self._c._subwindow.setClosable(self._c._closableWindow.booleanValue())


class CloseListener(ICloseListener):

    def __init__(self, c):
        self._c = c

    def windowClose(self, e):
        self._c.getWindow().showNotification('Window closed by user')
        self._c._openCloseButton.setCaption(self._c._openWindowText)


class ClickListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        if self._c._subwindow.getParent() is not None:
            self._c._subwindow.getParent().removeWindow(self._c._subwindow)
            self._c._openCloseButton.setCaption(self._c._openWindowText)
        else:
            self._c.getWindow().addWindow(self._c._subwindow)
            self._c._openCloseButton.setCaption(self._c._closeWindowText)
        return