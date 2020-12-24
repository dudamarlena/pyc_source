# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/WebLayoutExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Button, Label, HorizontalLayout, Tree, Window, Table
from muntjac.ui import window, button

class WebLayoutExample(VerticalLayout):

    def __init__(self):
        super(VerticalLayout, self).__init__()
        self._win = WebLayoutWindow()
        self._open = Button('Open sample in subwindow')
        self.setMargin(True)
        self._win.setWidth('70%')
        self._win.setHeight('70%')
        self._win.center()
        self._win.addListener(WindowListener(self), window.ICloseListener)
        self.addComponent(self._open)
        self._open.addListener(OpenListener(self), button.IClickListener)
        self.addComponent(Label("Don't worry: the content of the window is not supposed to make sense..."))


class WindowListener(window.ICloseListener):

    def __init__(self, c):
        self._c = c

    def windowClose(self, e):
        self._c._open.setEnabled(True)


class OpenListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.getWindow().addWindow(self._c._win)
        self._c._open.setEnabled(False)


class WebLayoutWindow(Window):

    def __init__(self):
        super(WebLayoutWindow, self).__init__()
        main = HorizontalLayout()
        main.setMargin(True)
        main.setSpacing(True)
        self.setContent(main)
        tree = Tree()
        tree.setContainerDataSource(ExampleUtil.getHardwareContainer())
        tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        for idd in tree.rootItemIds():
            tree.expandItemsRecursively(idd)

        self.addComponent(tree)
        left = VerticalLayout()
        left.setSpacing(True)
        self.addComponent(left)
        tbl = Table()
        tbl.setWidth('500px')
        tbl.setContainerDataSource(ExampleUtil.getISO3166Container())
        tbl.setSortDisabled(True)
        tbl.setPageLength(7)
        left.addComponent(tbl)
        text = Label(ExampleUtil.lorem, Label.CONTENT_XHTML)
        text.setWidth('500px')
        left.addComponent(text)