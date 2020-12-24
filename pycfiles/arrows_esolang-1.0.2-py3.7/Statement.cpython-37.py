# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrows_esolang/Statement.py
# Compiled at: 2019-10-31 01:48:48
# Size of source mod 2**32: 701 bytes
from enum import Enum
import arrows_esolang.Action as A
__statement_label__ = 0

class NodeType(Enum):
    ACTION = 0
    CONDITIONAL = 1


class Statement(object):

    def __init__(self):
        global __statement_label__
        self.kind = None
        self.if_zero = None
        self.if_else = None
        self.next = None
        self.actions = []
        self.label = __statement_label__
        __statement_label__ += 1

    def add_add(self, register):
        if register > 0:
            self.actions.append(A.Action(A.ActionType.ADD, register))

    def add_action(self, kind, register):
        self.add_add(register)
        self.actions.append(A.Action(kind))