# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop27.py
# Compiled at: 2020-05-02 07:08:15
"""Bytecode Interpreter operations for Python 2.7
"""
from __future__ import print_function, division
from xpython.byteop.byteop25 import ByteOp25
from xpython.byteop.byteop26 import ByteOp26
del ByteOp25.JUMP_IF_FALSE
del ByteOp25.JUMP_IF_TRUE

class ByteOp27(ByteOp26):

    def __init__(self, vm):
        self.vm = vm
        self.version = 2.7

    def BUILD_SET(self, count):
        """Works as BUILD_TUPLE, but creates a set. New in version 2.7"""
        elts = self.vm.popn(count)
        self.vm.push(set(elts))

    def JUMP_FORWARD(self, delta):
        """Increments bytecode counter by delta."""
        self.vm.jump(delta)

    def POP_JUMP_IF_TRUE(self, target):
        """If TOS is true, sets the bytecode counter to target. TOS is popped."""
        val = self.vm.pop()
        if val:
            self.vm.jump(target)

    def POP_JUMP_IF_FALSE(self, target):
        """If TOS is false, sets the bytecode counter to target. TOS is popped."""
        val = self.vm.pop()
        if not val:
            self.vm.jump(target)

    def JUMP_IF_TRUE_OR_POP(self, target):
        """
        If TOS is true, sets the bytecode counter to target and leaves TOS
        on the stack. Otherwise (TOS is false), TOS is popped.
        """
        val = self.vm.top()
        if val:
            self.vm.jump(target)
        else:
            self.vm.pop()

    def JUMP_IF_FALSE_OR_POP(self, target):
        """
        If TOS is false, sets the bytecode counter to target and leaves TOS
        on the stack. Otherwise (TOS is true), TOS is popped.
        """
        val = self.vm.top()
        if not val:
            self.vm.jump(target)
        else:
            self.vm.pop()

    def JUMP_ABSOLUTE(self, target):
        self.vm.jump(target)