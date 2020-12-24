# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/NativeWindowExample.py
# Compiled at: 2013-04-04 15:36:38
from datetime import datetime
from muntjac.demo.sampler.features.windows.NativeWindow import NativeWindow
from muntjac.api import VerticalLayout
from muntjac.api import Window, Label, Button, Link
from muntjac.ui.window import ICloseListener
from muntjac.ui import button
from muntjac.terminal.external_resource import ExternalResource

class NativeWindowExample(VerticalLayout):

    def __init__(self):
        super(NativeWindowExample, self).__init__()
        self.setSpacing(True)
        opn = Button('Open native window', OpenListener(self))
        self.addComponent(opn)
        openSampler = Link('Open Sampler in a new window', ExternalResource('#'), '_blank', 700, 500, Link.TARGET_BORDER_NONE)
        self.addComponent(openSampler)


class OpenListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        window = NativeWindow()
        self._c.getApplication().addWindow(window)
        self._c.getWindow().open(ExternalResource(window.getURL()), '_blank', 500, 200, Window.BORDER_NONE)


class NativeWindow(Window):

    def __init__(self):
        super(NativeWindow, self).__init__()
        layout = self.getContent()
        layout.setMargin(True)
        layout.setSpacing(True)
        message = Label('This is a native window, created at ' + str(datetime.today()))
        self.addComponent(message)
        self.addListener(WindowCloseListener(self), ICloseListener)


class WindowCloseListener(ICloseListener):

    def __init__(self, w):
        self._w = w

    def windowClose(self, e):
        self._w.getApplication().removeWindow(self._w)