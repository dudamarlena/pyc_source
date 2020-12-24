# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/buttons/CheckBoxesExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, CheckBox
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.button import IClickListener

class CheckBoxesExample(VerticalLayout, IClickListener):
    _CAPTION = 'Allow HTML'
    _TOOLTIP = 'Allow/disallow HTML in comments'
    _ICON = ThemeResource('../sampler/icons/page_code.gif')

    def __init__(self):
        super(CheckBoxesExample, self).__init__()
        self.setSpacing(True)
        cb = CheckBox(self._CAPTION)
        cb.setDescription(self._TOOLTIP)
        cb.setImmediate(True)
        cb.addListener(self, IClickListener)
        self.addComponent(cb)
        cb = CheckBox(self._CAPTION)
        cb.setDescription(self._TOOLTIP)
        cb.setIcon(self._ICON)
        cb.setImmediate(True)
        cb.addListener(self, IClickListener)
        self.addComponent(cb)
        cb = CheckBox()
        cb.setDescription(self._TOOLTIP)
        cb.setIcon(self._ICON)
        cb.setImmediate(True)
        cb.addListener(self, IClickListener)
        self.addComponent(cb)

    def buttonClick(self, event):
        enabled = event.getButton().booleanValue()
        self.getWindow().showNotification('HTML ' + ('enabled' if enabled else 'disabled'))