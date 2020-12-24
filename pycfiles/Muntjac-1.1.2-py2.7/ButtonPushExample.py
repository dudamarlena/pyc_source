# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/buttons/ButtonPushExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import HorizontalLayout, VerticalLayout, Button, NativeButton, Label
from muntjac.ui.button import IClickListener
from muntjac.terminal.theme_resource import ThemeResource

class ButtonPushExample(HorizontalLayout, IClickListener):
    _CAPTION = 'Save'
    _TOOLTIP = 'Save changes'
    _ICON = ThemeResource('../sampler/icons/action_save.gif')
    _NOTIFICATION = 'Changes have been saved'

    def __init__(self):
        super(ButtonPushExample, self).__init__()
        buttons = VerticalLayout()
        buttons.setSpacing(True)
        buttons.setMargin(False, True, False, False)
        self.addComponent(buttons)
        buttons.addComponent(Label('<h3>Normal buttons</h3>', Label.CONTENT_XHTML))
        b = Button(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.addListener(self, IClickListener)
        buttons.addComponent(b)
        b = Button(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)
        buttons.addComponent(b)
        b = Button()
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)
        buttons.addComponent(b)
        buttons = VerticalLayout()
        buttons.setSpacing(True)
        buttons.setMargin(False, False, False, True)
        self.addComponent(buttons)
        buttons.addComponent(Label('<h3>Native buttons</h3>', Label.CONTENT_XHTML))
        b = NativeButton(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.addListener(self, IClickListener)
        buttons.addComponent(b)
        b = NativeButton(self._CAPTION)
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)
        buttons.addComponent(b)
        b = NativeButton()
        b.setDescription(self._TOOLTIP)
        b.setIcon(self._ICON)
        b.addListener(self, IClickListener)
        buttons.addComponent(b)

    def buttonClick(self, event):
        self.getWindow().showNotification(self._NOTIFICATION)