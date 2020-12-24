# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/arrows_esolang/Interpreter.py
# Compiled at: 2019-10-31 01:48:36
# Size of source mod 2**32: 1551 bytes
import arrows_esolang.Util as U
import arrows_esolang.Action as A
import sys

def interpret(prog):
    register = 0
    lstack = [0]
    rstack = [0]
    while True:
        if prog.kind == A.NodeType.CONDITIONAL:
            if register == 0:
                prog = prog.if_zero
            else:
                prog = prog.if_else
        else:
            for a in prog.actions:
                if a.kind == U.ActionType.END:
                    sys.exit(register)
                elif a.kind == A.ActionType.ADD:
                    register += a.value
                elif a.kind == A.ActionType.PUSH_LEFT:
                    lstack.append(register)
                elif a.kind == A.ActionType.PUSH_RIGHT:
                    rstack.append(register)
                else:
                    if a.kind == A.ActionType.SUBTRACT_LEFT:
                        register -= lstack.pop()
                        if not lstack:
                            lstack.append(0)

            prog = prog.next