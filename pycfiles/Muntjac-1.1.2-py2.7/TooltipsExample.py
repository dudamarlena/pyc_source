# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/TooltipsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Button, RichTextArea
from muntjac.ui.themes import BaseTheme
from muntjac.ui.button import IClickListener

class TooltipsExample(VerticalLayout):
    _editTxt = 'Edit tooltip'
    _applyTxt = 'Apply'

    def __init__(self):
        super(TooltipsExample, self).__init__()
        self.setSpacing(True)
        plain = Button('Mouse over for plain tooltip')
        plain.setStyleName(BaseTheme.BUTTON_LINK)
        plain.setDescription('A simple plaintext tooltip')
        self.addComponent(plain)
        rich = Button('Mouse over for richtext tooltip')
        rich.setStyleName(BaseTheme.BUTTON_LINK)
        rich.setDescription('<h2><img src="../VAADIN/themes/sampler/icons/comment_yellow.gif"/>A richtext tooltip</h2><ul><li>HTML formatting</li><li>Images<br/></li><li>etc...</li></ul>')
        self.addComponent(rich)
        rte = RichTextArea()
        rte.setValue('Click <b>' + self._editTxt + '</b> to edit this tooltip, then <b>' + self._applyTxt + '</b>')
        rte.setVisible(False)
        rte.setWidth('100%')
        self.addComponent(rte)
        aply = Button(self._editTxt, EditListener(self, rte))
        aply.setDescription(rte.getValue())
        self.addComponent(aply)


class EditListener(IClickListener):

    def __init__(self, component, rte):
        self._component = component
        self._rte = rte

    def buttonClick(self, event):
        if self._rte.isVisible():
            self._rte.setVisible(False)
            event.getButton().setDescription(self._rte.getValue())
            event.getButton().setCaption(self._component._editTxt)
        else:
            self._rte.setVisible(True)
            event.getButton().setCaption(self._component._applyTxt)