# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/ClickableLayoutBasicExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label, GridLayout, TextField, Select, Link
from muntjac.event.layout_events import ILayoutClickListener
from muntjac.util import fullname

class ClickableLayoutBasicExample(VerticalLayout):

    def __init__(self):
        super(ClickableLayoutBasicExample, self).__init__()
        self.setMargin(True)
        self.setSpacing(True)
        self.addComponent(self.createVerticalClickableLayout())
        self.addComponent(self.createChildComponentClickableLayout())
        self.addComponent(self.createKeyRegisterClickableLayout())

    def createVerticalClickableLayout(self):
        layout = VerticalLayout()
        layout.setWidth('90%')
        layout.setSpacing(True)
        layout.addStyleName('border')
        layout.setMargin(True)
        layout.addComponent(Label('<b>This is a vertical layout with a click listener attached. Try clicking anywhere inside this layout.</b>', Label.CONTENT_RAW))
        clickX = Label('X-coordinate: <i>Not available.</i>', Label.CONTENT_RAW)
        layout.addComponent(clickX)
        clickY = Label('Y-coordinate: <i>Not available.</i>', Label.CONTENT_RAW)
        layout.addComponent(clickY)
        clickRelativeX = Label('X-coordinate relative to the layout: <i>Not available.</i>', Label.CONTENT_RAW)
        layout.addComponent(clickRelativeX)
        clickRelativeY = Label('Y-coordinate relative to the layout: <i>Not available.</i>', Label.CONTENT_RAW)
        layout.addComponent(clickRelativeY)
        button = Label('Mouse button: <i>Not available.</i>', Label.CONTENT_RAW)
        layout.addComponent(button)
        layout.addListener(LayoutListener(self, button, clickX, clickY, clickRelativeX, clickRelativeY), ILayoutClickListener)
        return layout

    def createChildComponentClickableLayout(self):
        layout = GridLayout(5, 2)
        layout.addStyleName('border')
        layout.setSpacing(True)
        layout.setWidth('90%')
        layout.setMargin(True)
        layout.addComponent(Label('<b>Clickable layout events include a reference to the child component beneath the click. Try clicking anywhere in this layout.</b>', Label.CONTENT_RAW), 0, 0, 4, 0)
        layout.addComponent(TextField(None, 'Click here'))
        layout.addComponent(Link('Click here', None))
        select = Select(None, ['Click here'])
        select.select('Click here')
        layout.addComponent(select)
        layout.addListener(GridListener(self), ILayoutClickListener)
        return layout

    def createKeyRegisterClickableLayout(self):
        layout = VerticalLayout()
        layout.setWidth('90%')
        layout.setSpacing(True)
        layout.addStyleName('border')
        layout.setMargin(True)
        layout.addComponent(Label('<b>Layout click events register if control keys are pressed during the click and double clicks. Try clicking anywhere inside this layout while holding CTRL, ALT, SHIFT or META key down.</b>', Label.CONTENT_RAW))
        layout.addListener(VerticalListener(self), ILayoutClickListener)
        return layout


class LayoutListener(ILayoutClickListener):

    def __init__(self, c, button, clickX, clickY, clickRelativeX, clickRelativeY):
        self._button = button
        self._c = c
        self._clickX = clickX
        self._clickY = clickY
        self._clickRelativeX = clickRelativeX
        self._clickRelativeY = clickRelativeY

    def layoutClick(self, event):
        self._clickX.setValue('X-coordinate: %d' % event.getClientX())
        self._clickY.setValue('Y-coordinate: %d' % event.getClientY())
        self._clickRelativeX.setValue('X-coordinate relative to the layout: %d' % event.getRelativeX())
        self._clickRelativeY.setValue('Y-coordinate relative to the layout: %d' % event.getRelativeY())
        self._button.setValue('Mouse button: ' + event.getButtonName())
        self._c.getWindow().showNotification('Layout clicked!')


class GridListener(ILayoutClickListener):

    def __init__(self, c):
        self._c = c

    def layoutClick(self, event):
        child = event.getChildComponent()
        if child is None:
            self._c.getWindow().showNotification('The click was not over any component.')
        else:
            self._c.getWindow().showNotification('The click was over a ' + fullname(child))
        return


class VerticalListener(ILayoutClickListener):

    def __init__(self, c):
        self._c = c

    def layoutClick(self, event):
        message = ''
        if event.isCtrlKey():
            message += 'CTRL+'
        if event.isAltKey():
            message += 'ALT+'
        if event.isShiftKey():
            message += 'SHIFT+'
        if event.isMetaKey():
            message += 'META+'
        if event.isDoubleClick():
            message += 'DOUBLE CLICK'
        else:
            message += 'CLICK'
        self._c.getWindow().showNotification(message)