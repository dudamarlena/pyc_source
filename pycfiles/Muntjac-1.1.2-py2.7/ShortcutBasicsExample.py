# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/shortcuts/ShortcutBasicsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, TextField, Button
from muntjac.ui.abstract_field import FocusShortcut
from muntjac.event.shortcut_action import KeyCode, ModifierKey
from muntjac.ui.button import IClickListener

class ShortcutBasicsExample(VerticalLayout):

    def __init__(self):
        super(ShortcutBasicsExample, self).__init__()
        self.setSpacing(True)
        firstname = TextField('Firstname')
        firstname.setInputPrompt('ALT-SHIFT-F to focus')
        self.addComponent(firstname)
        firstname.addShortcutListener(FocusShortcut(firstname, KeyCode.F, ModifierKey.ALT, ModifierKey.SHIFT))
        lastname = TextField('Lastname')
        lastname.setInputPrompt('ALT-SHIFT-L to focus')
        self.addComponent(lastname)
        lastname.addShortcutListener(FocusShortcut(lastname, KeyCode.L, ModifierKey.ALT, ModifierKey.SHIFT))
        enter = Button('Enter', EnterListener(self))
        self.addComponent(enter)
        enter.setStyleName('primary')
        enter.setClickShortcut(KeyCode.ENTER)


class EnterListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.getWindow().showNotification('Enter button clicked')