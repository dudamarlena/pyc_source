# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/shortcuts/ShortcutScopeExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, HorizontalLayout, Panel, TextField, Button
from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.ui.component import IFocusable
from muntjac.ui.abstract_field import FocusShortcut
from muntjac.event.shortcut_action import KeyCode, ModifierKey
from muntjac.ui.button import ClickShortcut, IClickListener

class ShortcutScopeExample(VerticalLayout):

    def __init__(self):
        super(ShortcutScopeExample, self).__init__()
        self.setSpacing(True)
        hz = HorizontalLayout()
        hz.setSpacing(True)
        self.addComponent(hz)
        hz.addComponent(self.createPanel(1))
        hz.addComponent(self.createPanel(2))

    def createPanel(self, number):
        p = Panel('Panel %d' % number)
        p.getContent().setSpacing(True)
        p.addAction(NextFieldListener('Next field', KeyCode.ARROW_DOWN, None))
        firstname = TextField('Firstname')
        firstname.setInputPrompt('ALT-SHIFT-F to focus')
        p.addComponent(firstname)
        p.addAction(FocusShortcut(firstname, KeyCode.F, ModifierKey.ALT, ModifierKey.SHIFT))
        firstname.addShortcutListener(FocusShortcut(firstname, 'Focus panel &_' + str(number)))
        p.setDescription('CTRL-' + str(number) + ' to focus')
        lastname = TextField('Lastname')
        lastname.setInputPrompt('ALT-SHIFT-L to focus')
        p.addComponent(lastname)
        p.addAction(FocusShortcut(lastname, KeyCode.L, ModifierKey.ALT, ModifierKey.SHIFT))
        save = Button('Save', SaveListener(self, p))
        p.addComponent(save)
        p.addAction(ClickShortcut(save, KeyCode.S, ModifierKey.ALT, ModifierKey.SHIFT))
        return p


class NextFieldListener(ShortcutListener):

    def handleAction(self, sender, target):
        for nxt in sender.getComponentIterator():
            if isinstance(nxt, IFocusable):
                nxt.focus()


class SaveListener(IClickListener):

    def __init__(self, c, panel):
        self._c = c
        self._panel = panel

    def buttonClick(self, event):
        self._c.getWindow().showNotification(self._panel.getCaption() + ' save clicked')