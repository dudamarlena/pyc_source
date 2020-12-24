# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/buttons/ButtonLinkExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Button
from muntjac.ui.themes import BaseTheme
from muntjac.ui import button
from muntjac.terminal.theme_resource import ThemeResource

class ButtonLinkExample(VerticalLayout, button.IClickListener):
    _CAPTION = 'Help'
    _TOOLTIP = 'Show help'
    _ICON = ThemeResource('../sampler/icons/icon_info.gif')
    _NOTIFICATION = 'Help clicked'

    def __init__(self):
        super(ButtonLinkExample, self).__init__()
        self.setSpacing(True)
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.addListener(self, button.IClickListener)
        self.addComponent(b)
        b = Button(self._CAPTION)
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, button.IClickListener)
        self.addComponent(b)
        b = Button()
        b.setStyleName(BaseTheme.BUTTON_LINK)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, button.IClickListener)
        self.addComponent(b)

    def buttonClick(self, event):
        self.getWindow().showNotification(self._NOTIFICATION)