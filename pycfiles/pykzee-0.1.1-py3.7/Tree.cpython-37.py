# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykzee/Tree.py
# Compiled at: 2019-10-25 08:08:53
# Size of source mod 2**32: 4181 bytes
import collections
from pyimmutable import ImmutableDict
from pykzee.common import Undefined, setDataForPath

class Tree:

    class RegisteredCommand:
        __slots__ = ('function', 'doc', 'unregister', 'disabled')

        def __init__(self, function, doc, unregister):
            self.function = function
            self.doc = doc
            self.unregister = unregister
            self.disabled = False

    TreeAccess = collections.namedtuple('TreeAccess', ('set', 'submitState', 'registerCommand',
                                                       'createSubtree', 'clear',
                                                       'deactivate'))

    def __init__(self, parent, path, *, immediate_updates=True):
        self._Tree__parentSet = parent.set
        self._Tree__parentRegisterCommand = parent.registerCommand
        self._Tree__path = path
        self._Tree__state = ImmutableDict()
        self._Tree__reportedState = Undefined
        self._Tree__registeredCommands = {}
        self._Tree__immediate_updates = immediate_updates
        self._Tree__deactivated = False
        self._Tree__hidden = False

    @property
    def path(self):
        return self._Tree__path

    def getAccessProxy(self):
        return self.TreeAccess(self.set, self.submitState, self.registerCommand, self.createSubtree, self.clear, self.deactivate)

    def set(self, path, value):
        self._Tree__state = setDataForPath(self._Tree__state, path, value)
        if self._Tree__immediate_updates:
            self.submitState()

    def registerCommand(self, path, name, function, doc=Undefined):
        if doc is Undefined:
            doc = function.__doc__
        else:
            existing_rc = self._Tree__registeredCommands.get((path, name))
            if existing_rc is not None:
                existing_rc.disabled = True
                existing_rc.unregister()
            if self._Tree__hidden:
                unregister = no_op
            else:
                unregister = self._Tree__parentRegisterCommand(self._Tree__path + path, name, function, doc)
        rc = self.RegisteredCommand(function, doc, unregister)
        self._Tree__registeredCommands[(path, name)] = rc

        def unregister_command():
            if not rc.disabled:
                rc.disabled = True
                del self._Tree__registeredCommands[(path, name)]
                rc.unregister()

        return unregister_command

    def createSubtree(self, path, *, immediate_updates=True):
        return Tree(self, path, immediate_updates=immediate_updates)

    def clear(self):
        for rc in self._Tree__registeredCommands.values():
            rc.disabled = True
            rc.unregister()

        self._Tree__registeredCommands = {}
        self._Tree__state = ImmutableDict()
        self._Tree__reportedState = Undefined
        self._Tree__parentSet(self._Tree__path, Undefined)

    def deactivate(self):
        if not self._Tree__deactivated:
            self.clear()
            self._Tree__parentSet = self._Tree__parentRegisterCommand = raise_deactivated
            self._Tree__deactivated = True

    def hide(self):
        if self._Tree__hidden:
            return
        for rc in self._Tree__registeredCommands.values():
            rc.unregister()
            rc.unregister = no_op

        self._Tree__parentSet(self._Tree__path, Undefined)
        self._Tree__hidden = True

    def show(self, new_path=None):
        if not self._Tree__hidden:
            if not new_path is None:
                if new_path == self._Tree__path:
                    return
        self.hide()
        if new_path is not None:
            self._Tree__path = new_path
        self._Tree__parentSet(self._Tree__path, self._Tree__state)
        self._Tree__hidden = False
        self._Tree__reportedState = self._Tree__state
        for (path, name), rc in self._Tree__registeredCommands.items():
            rc.unregister = self._Tree__parentRegisterCommand(self._Tree__path + path, name, rc.function, rc.doc)

    def submitState(self):
        if self._Tree__reportedState is not self._Tree__state:
            if not self._Tree__hidden:
                self._Tree__parentSet(self._Tree__path, self._Tree__state)
                self._Tree__reportedState = self._Tree__state


def raise_deactivated(*args, **kwargs):
    raise Exception('Subtree has been deactivated')


def no_op():
    pass