# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop37.py
# Compiled at: 2020-05-07 20:12:47
"""Bytecode Interpreter operations for Python 3.7
"""
from __future__ import print_function, division
import types
from xpython.byteop.byteop36 import ByteOp36
del ByteOp36.STORE_ANNOTATION

class ByteOp37(ByteOp36):

    def __init__(self, vm):
        super(ByteOp37, self).__init__(vm)

    def LOAD_METHOD(self, name):
        """Loads a method named co_names[namei] from the TOS object. TOS is
        popped. This bytecode distinguishes two cases: if TOS has a
        method with the correct name, the bytecode pushes the unbound
        method and TOS. TOS will be used as the first argument (self)
        by CALL_METHOD when calling the unbound method. Otherwise,
        NULL and the object return by the attribute lookup are pushed.

        rocky: In our implementation in Python we don't have NULL: all
        stack entries have *some* value. So instead we'll push another
        item: the status. Also, instead of pushing the unbound method
        and self, we will pass the bound method, since that is what we
        have here. So TOS (self) is not pushed back onto the stack.
        """
        TOS = self.vm.pop()
        if hasattr(TOS, name):
            self.vm.push(getattr(TOS, name))
            self.vm.push('LOAD_METHOD lookup success')
        else:
            self.vm.push('fill in attribute method lookup')
            self.vm.push(None)
        return

    def CALL_METHOD(self, count):
        """Calls a method. argc is the number of positional
        arguments. Keyword arguments are not supported. This opcode is
        designed to be used with LOAD_METHOD. Positional arguments are
        on top of the stack. Below them, the two items described in
        LOAD_METHOD are on the stack (either self and an unbound
        method object or NULL and an arbitrary callable). All of them
        are popped and the return value is pushed.

        rocky: In our setting, before "self" we have an additional
        item which is the status of the LOAD_METHOD. There is no way
        in Python to represent a value outside of a Python value which
        you can do in C, and is in effect what NULL is.
        """
        posargs = self.vm.popn(count)
        is_success = self.vm.pop()
        if is_success:
            func = self.vm.pop()
            self.call_function_with_args_resolved(func, posargs, {})
        else:
            raise self.vm.VMError('CALL_METHOD not implemented yet')