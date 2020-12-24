# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/action.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1836 bytes
from .ops import Ops
from .editor import Editor
from .receiver import Receiver
from ..util import deprecated

class Action(Receiver):
    __doc__ = '\n    An Action takes an incoming message, applies Ops to it, and then\n    uses it to set a value on a Editor.\n    '

    def __init__(self, address, ops=()):
        self.address = Editor(address)
        self.ops = Ops(*ops)

    def set_project(self, project):
        self.address.set_project(project)

    def receive(self, values):
        if self.ops:
            if len(values) == 1:
                values = [
                 self.ops(values[0])]
        return self.address.receive(values)

    def __bool__(self):
        return bool(self.address or self.ops)

    def __str__(self):
        if self.ops:
            return ('%s->%s' % self.address, self.ops)
        else:
            return str(self.address)

    @classmethod
    def make(cls, action):
        if isinstance(action, str):
            return cls(action)
        else:
            if isinstance(action, dict):
                return cls(**action)
            return cls(*action)


class ActionList(Receiver):
    __doc__ = 'A list of Actions.'

    def __init__(self, actions=None):
        if isinstance(actions, (str, dict)):
            actions = [
             actions]
        self.actions = tuple(Action.make(a) for a in actions or ())

    def set_project(self, project):
        for a in self.actions:
            a.set_project(project)

    def receive(self, msg):
        values = tuple(msg.values())
        for action in self.actions:
            action.receive(values)

    def __bool__(self):
        return bool(self.actions)

    def __str__(self):
        return ' + '.join(str(a) for a in self.actions)