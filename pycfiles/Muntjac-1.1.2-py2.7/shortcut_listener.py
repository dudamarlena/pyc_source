# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/shortcut_listener.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.event.action import IListener
from muntjac.event.shortcut_action import ShortcutAction

class ShortcutListener(ShortcutAction, IListener):

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 1:
            shorthandCaption, = args
            super(ShortcutListener, self).__init__(shorthandCaption)
        elif nargs == 2:
            shorthandCaption, modifierKeys = args
            super(ShortcutListener, self).__init__(shorthandCaption, modifierKeys)
        elif nargs == 3:
            caption, keyCode, modifierKeys = args
            super(ShortcutListener, self).__init__(caption, keyCode, modifierKeys)
        elif nargs == 4:
            caption, icon, keyCode, modifierKeys = args
            super(ShortcutListener, self).__init__(caption, icon, keyCode, modifierKeys)
        else:
            raise ValueError

    def handleAction(self, sender, target):
        pass