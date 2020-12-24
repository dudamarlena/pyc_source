# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/action_manager.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.event import action
from muntjac.terminal.key_mapper import KeyMapper
from muntjac.event.shortcut_action import ShortcutAction

class ActionManager(action.IHandler, action.INotifier):
    """Notes:

    Empties the keymapper for each repaint to avoid leaks; can cause problems
    in the future if the client assumes key don't change. (if lazyloading, one
    must not cache results)
    """

    def __init__(self, viewer=None):
        self.ownActions = None
        self.actionHandlers = None
        self.actionMapper = None
        self._clientHasActions = False
        self.viewer = viewer
        return

    def requestRepaint(self):
        if self.viewer is not None:
            self.viewer.requestRepaint()
        return

    def setViewer(self, viewer):
        if viewer == self.viewer:
            return
        else:
            if self.viewer is not None:
                self.viewer.removeActionHandler(self)
            self.requestRepaint()
            if viewer is not None:
                viewer.addActionHandler(self)
            self.viewer = viewer
            self.requestRepaint()
            return

    def addAction(self, action):
        if self.ownActions is None:
            self.ownActions = set()
        if self.ownActions.add(action):
            self.requestRepaint()
        return

    def removeAction(self, action):
        if self.ownActions is not None:
            if self.ownActions.remove(action):
                self.requestRepaint()
        return

    def addActionHandler(self, actionHandler):
        if actionHandler == self:
            return
        else:
            if actionHandler is not None:
                if self.actionHandlers is None:
                    self.actionHandlers = set()
                if actionHandler not in self.actionHandlers:
                    self.actionHandlers.add(actionHandler)
                    self.requestRepaint()
            return

    def removeActionHandler(self, actionHandler):
        if self.actionHandlers is not None and actionHandler in self.actionHandlers:
            if self.actionHandlers.remove(actionHandler):
                self.requestRepaint()
            if len(self.actionHandlers) == 0:
                self.actionHandlers = None
        return

    def removeAllActionHandlers(self):
        if self.actionHandlers is not None:
            self.actionHandlers = None
            self.requestRepaint()
        return

    def paintActions(self, actionTarget, paintTarget):
        self.actionMapper = None
        actions = set()
        if self.actionHandlers is not None:
            for handler in self.actionHandlers:
                ac = handler.getActions(actionTarget, self.viewer)
                if ac is not None:
                    for a in ac:
                        actions.add(a)

        if self.ownActions is not None:
            actions = actions.union(self.ownActions)
        if len(actions) > 0 or self._clientHasActions:
            self.actionMapper = KeyMapper()
            paintTarget.addVariable(self.viewer, 'action', '')
            paintTarget.startTag('actions')
            for a in actions:
                paintTarget.startTag('action')
                akey = self.actionMapper.key(a)
                paintTarget.addAttribute('key', akey)
                if a.getCaption() is not None:
                    paintTarget.addAttribute('caption', a.getCaption())
                if a.getIcon() is not None:
                    paintTarget.addAttribute('icon', a.getIcon())
                if isinstance(a, ShortcutAction):
                    sa = a
                    paintTarget.addAttribute('kc', sa.getKeyCode())
                    modifiers = sa.getModifiers()
                    if modifiers is not None:
                        smodifiers = [
                         None] * len(modifiers)
                        for i in range(len(modifiers)):
                            smodifiers[i] = str(modifiers[i])

                        paintTarget.addAttribute('mk', smodifiers)
                paintTarget.endTag('action')

            paintTarget.endTag('actions')
        self._clientHasActions = len(actions) > 0
        return

    def handleActions(self, variables, sender):
        if 'action' in variables and self.actionMapper is not None:
            key = variables.get('action')
            a = self.actionMapper.get(key)
            target = variables.get('actiontarget')
            if a is not None:
                self.handleAction(a, sender, target)
        return

    def getActions(self, target, sender):
        actions = set()
        if self.ownActions is not None:
            for a in self.ownActions:
                actions.add(a)

        if self.actionHandlers is not None:
            for h in self.actionHandlers:
                as_ = h.getActions(target, sender)
                if as_ is not None:
                    for a in as_:
                        actions.add(a)

        return list(actions)

    def handleAction(self, a, sender, target):
        if self.actionHandlers is not None:
            arry = list(self.actionHandlers)
            for handler in arry:
                handler.handleAction(a, sender, target)

        if self.ownActions is not None and a in self.ownActions and isinstance(a, action.IListener):
            a.handleAction(sender, target)
        return