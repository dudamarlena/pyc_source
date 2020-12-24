# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop33.py
# Compiled at: 2020-05-07 20:07:23
"""Byte Interpreter operations for Python 3.3
"""
from __future__ import print_function, division
from xpython.byteop.byteop32 import ByteOp32
from xpython.pyobj import Generator

class ByteOp33(ByteOp32):

    def __init__(self, vm):
        super(ByteOp33, self).__init__(vm)

    def YIELD_FROM(self):
        """
        Pops TOS and delegates to it as a subiterator from a generator.
        """
        u = self.vm.pop()
        x = self.vm.top()
        try:
            if not isinstance(x, Generator) or u is None:
                retval = next(x)
            else:
                retval = x.send(u)
            self.vm.return_value = retval
        except StopIteration as e:
            self.vm.pop()
            self.vm.push(e.value)
        else:
            self.vm.jump(self.vm.frame.f_lasti - 1)
            return 'yield'

        return


if __name__ == '__main__':
    x = ByteOp33(None)